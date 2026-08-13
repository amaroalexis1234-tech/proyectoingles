import logging
import uuid

from sqlmodel import Session, select

from app.core.config import settings
from app.modules.ai.models import AiExplanationCache
from app.modules.ai.schemas import ExplanationPayload
from app.modules.auth.models import User
from app.modules.evaluations.models import TestAttempt
from app.modules.evaluations.service import get_completed_result
from app.modules.question_bank.models import Passage, Question, Section
from app.shared.exceptions import DomainError

logger = logging.getLogger(__name__)

FALLBACK_MESSAGE = (
    "No hay una explicación generada por IA disponible en este momento. "
    "Revisa la respuesta correcta señalada arriba junto con la explicación base de la pregunta."
)

SECTION_LABELS = {
    "structure": "Structure",
    "written_expression": "Written Expression",
    "reading": "Reading",
    "vocabulary": "Vocabulary",
}


class QuestionNotFoundError(DomainError):
    def __init__(self) -> None:
        super().__init__("La pregunta no existe.")


def _fallback_payload(question: Question) -> ExplanationPayload:
    # Unico lugar donde se construye el fallback: siempre solo `explanation`,
    # el resto de los campos quedan None -- nunca se fabrica evidencia,
    # vocabulario, regla gramatical ni traduccion que la IA no genero.
    return ExplanationPayload(explanation=question.explanation or FALLBACK_MESSAGE)


def _build_prompt(question: Question, student_answer: str | None, passage: Passage | None) -> str:
    options_text = "\n".join(f"{key}) {value}" for key, value in question.options.items())
    student_line = f"\nThe student answered: {student_answer}" if student_answer else ""

    wants_evidence = question.section == Section.reading and passage is not None
    wants_grammar_rule = question.section in (Section.structure, Section.written_expression)

    # Todo el contenido pedido es en ingles a proposito (decision del usuario:
    # inmersion total, sin puente al español) -- "translation" y el campo
    # "translation" de vocabulary_terms se repropusieron como parafraseo/
    # definicion en ingles simple, ya no traduccion al español.
    fields = [
        '- "explanation": 2-3 clear, direct sentences in English explaining why that is the '
        "correct answer. If the student picked an incorrect option, briefly explain why that "
        "specific option is wrong.",
        '- "vocabulary_terms": a list of 1 to 3 key terms from the question, each with its '
        '"term" and a "translation" field containing a short, simple English definition or '
        "synonym for that term (not a translation into another language).",
        '- "translation": a simple English paraphrase of the relevant sentence or question, '
        "using easier words than the original.",
    ]
    if wants_evidence:
        fields.append(
            '- "evidence": a short direct quote (one sentence) from the passage that supports '
            "the correct answer."
        )
    if wants_grammar_rule:
        fields.append('- "grammar_rule": the name or brief description of the applicable grammar rule.')

    passage_block = f"\n\nPassage:\n{passage.text}" if wants_evidence and passage else ""

    return (
        "You are an English tutor preparing Mexican students for the TOEFL ITP exam "
        "(target score 550).\n\n"
        f"Section: {question.section.value}\n"
        f"Question: {question.prompt}\n\n"
        f"Options:\n{options_text}\n\n"
        f"Correct answer: {question.correct_answer}{student_line}"
        f"{passage_block}\n\n"
        "Respond in JSON with exactly these fields, with all content written in English:\n"
        + "\n".join(fields)
    )


EXPLANATION_TOOL = {
    "name": "provide_explanation",
    "description": "Entrega la explicación estructurada de la respuesta correcta.",
    "input_schema": {
        "type": "object",
        "properties": {
            "explanation": {
                "type": "string",
                "description": "2-3 oraciones claras y directas en español.",
            },
            "evidence": {
                "type": "string",
                "description": "Cita textual corta del passage que respalda la respuesta (solo Reading).",
            },
            "vocabulary_terms": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "term": {"type": "string"},
                        "translation": {"type": "string"},
                    },
                    "required": ["term", "translation"],
                },
            },
            "grammar_rule": {
                "type": "string",
                "description": "Nombre o descripción breve de la regla gramatical aplicable.",
            },
            "translation": {
                "type": "string",
                "description": "Traducción al español de la oración/pregunta relevante.",
            },
        },
        "required": ["explanation"],
    },
}


def explain_question(
    session: Session, question_id: uuid.UUID, student_answer: str | None
) -> tuple[ExplanationPayload, str]:
    question = session.get(Question, question_id)
    if question is None:
        raise QuestionNotFoundError()

    passage = session.get(Passage, question.passage_id) if question.passage_id else None
    normalized_answer = student_answer or ""

    cached = session.exec(
        select(AiExplanationCache).where(
            AiExplanationCache.question_id == question_id,
            AiExplanationCache.student_answer == normalized_answer,
        )
    ).first()
    if cached is not None:
        return ExplanationPayload.model_validate(cached.payload), "ai"

    # Sin API key configurada: no se intenta llamar a Claude, se usa la
    # explicacion pre-guardada de la pregunta (si existe) como fallback
    # honesto -- nunca se simula una respuesta de IA.
    if not settings.ANTHROPIC_API_KEY:
        return _fallback_payload(question), "fallback"

    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        prompt = _build_prompt(question, student_answer, passage)
        response = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=1024,
            tools=[EXPLANATION_TOOL],
            tool_choice={"type": "tool", "name": "provide_explanation"},
            messages=[{"role": "user", "content": prompt}],
        )
        tool_use = next(block for block in response.content if block.type == "tool_use")
        payload = ExplanationPayload.model_validate(tool_use.input)
        if not payload.explanation.strip():
            raise ValueError("Respuesta vacía o invalida de Claude")

        session.add(
            AiExplanationCache(
                question_id=question_id, student_answer=normalized_answer, payload=payload.model_dump()
            )
        )
        session.commit()
        return payload, "ai"
    except Exception:
        logger.exception("Fallo la llamada a Claude, usando fallback")
        return _fallback_payload(question), "fallback"


def _weakest_section(attempt: TestAttempt) -> tuple[str, float] | None:
    """(label, accuracy_percent) de la seccion con menor precision -- solo
    considera secciones con al menos una pregunta, dato real de section_scores."""
    worst: tuple[str, float] | None = None
    for section, score in attempt.section_scores.items():
        total = score.get("total", 0)
        if total == 0:
            continue
        accuracy = score["correct"] / total * 100
        if worst is None or accuracy < worst[1]:
            worst = (SECTION_LABELS.get(section, section), round(accuracy, 1))
    return worst


def _fallback_recommendation(attempt: TestAttempt) -> str:
    weakest = _weakest_section(attempt)
    if weakest is None:
        return "Completa más preguntas para recibir recomendaciones personalizadas de práctica."
    label, pct = weakest
    return (
        f"Tu desempeño más bajo fue en {label} ({pct}%). "
        "Te recomendamos enfocar tu práctica ahí antes del siguiente intento."
    )


def recommend_practice(session: Session, user: User, attempt_id: uuid.UUID) -> tuple[str, str]:
    attempt = get_completed_result(session, user, attempt_id)
    fallback_text = _fallback_recommendation(attempt)

    if attempt.ai_recommendation:
        return attempt.ai_recommendation, "ai"

    if not settings.ANTHROPIC_API_KEY:
        return fallback_text, "fallback"

    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        scores_text = "\n".join(
            f"- {SECTION_LABELS.get(section, section)}: {score['correct']}/{score['total']}"
            for section, score in attempt.section_scores.items()
            if score.get("total", 0) > 0
        )
        prompt = (
            "You are an English tutor preparing Mexican students for the TOEFL ITP exam "
            "(target score 550). A student just completed an evaluation with this score "
            f"breakdown by section:\n{scores_text}\n\n"
            "Write a short recommendation (2-3 sentences, in English, encouraging tone) about "
            "which section they should focus their next practice on and why. Do not use markdown."
        )
        response = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        text_block = next(block for block in response.content if block.type == "text")
        text = text_block.text.strip()
        if not text:
            raise ValueError("Respuesta vacía de Claude")

        attempt.ai_recommendation = text
        session.add(attempt)
        session.commit()
        return text, "ai"
    except Exception:
        logger.exception("Fallo la llamada a Claude, usando fallback")
        return fallback_text, "fallback"
