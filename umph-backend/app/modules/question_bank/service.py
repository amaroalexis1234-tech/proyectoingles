import csv
import io
import uuid

from sqlmodel import Session, select

from app.modules.ai.models import AiExplanationCache
from app.modules.auth.models import User
from app.modules.question_bank.models import Passage, Question, QuestionType, Section
from app.modules.question_bank.schemas import PassageCreate, QuestionCreate, QuestionUpdate
from app.shared.exceptions import DomainError


def _clear_explanation_cache(session: Session, question_id: uuid.UUID) -> None:
    """El maestro edito o borro la pregunta -- cualquier explicacion de IA
    cacheada para ella ya no aplica, se descarta para no servir algo obsoleto."""
    cached = session.exec(select(AiExplanationCache).where(AiExplanationCache.question_id == question_id)).all()
    for entry in cached:
        session.delete(entry)


class QuestionNotFoundError(DomainError):
    def __init__(self) -> None:
        super().__init__("La pregunta no existe.")


class PassageNotFoundError(DomainError):
    def __init__(self) -> None:
        super().__init__("El passage no existe.")


REQUIRED_CSV_COLUMNS = {
    "section",
    "question_type",
    "prompt",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "correct_answer",
}
VALID_SECTIONS = {s.value for s in Section}
VALID_QUESTION_TYPES = {t.value for t in QuestionType}


def create_passage(session: Session, teacher: User, data: PassageCreate) -> Passage:
    passage = Passage(title=data.title, text=data.text, source=data.source)
    session.add(passage)
    session.commit()
    session.refresh(passage)
    return passage


def list_passages(session: Session) -> list[Passage]:
    return list(session.exec(select(Passage)).all())


def create_question(session: Session, teacher: User, data: QuestionCreate) -> Question:
    if data.passage_id is not None and session.get(Passage, data.passage_id) is None:
        raise PassageNotFoundError()

    question = Question(
        section=data.section,
        question_type=data.question_type,
        prompt=data.prompt,
        options=data.options,
        correct_answer=data.correct_answer,
        explanation=data.explanation,
        passage_id=data.passage_id,
        # El maestro ES la fuente de verdad (a diferencia de preguntas
        # extraidas de un PDF sin answer key confirmado) -- verified=True.
        verified=True,
        source=f"Creado por {teacher.full_name}",
    )
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


def list_questions(session: Session, section: Section | None) -> list[Question]:
    statement = select(Question)
    if section is not None:
        statement = statement.where(Question.section == section)
    return list(session.exec(statement).all())


def get_question(session: Session, question_id: uuid.UUID) -> Question:
    question = session.get(Question, question_id)
    if question is None:
        raise QuestionNotFoundError()
    return question


def update_question(session: Session, question_id: uuid.UUID, data: QuestionUpdate) -> Question:
    question = get_question(session, question_id)

    if data.passage_id is not None and session.get(Passage, data.passage_id) is None:
        raise PassageNotFoundError()

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(question, field, value)

    _clear_explanation_cache(session, question_id)
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


def delete_question(session: Session, question_id: uuid.UUID) -> None:
    question = get_question(session, question_id)
    _clear_explanation_cache(session, question_id)
    session.delete(question)
    session.commit()


def _parse_csv_row(row: dict[str, str], passages_by_title: dict[str, Passage]) -> Question:
    """Lanza ValueError con un mensaje claro si la fila no es valida -- nunca
    inventa o adivina un valor, cada campo requerido debe venir explicito."""
    section_raw = (row.get("section") or "").strip().lower()
    if section_raw not in VALID_SECTIONS:
        raise ValueError(f"section inválida: '{section_raw}' (usa: {', '.join(sorted(VALID_SECTIONS))})")

    question_type_raw = (row.get("question_type") or "").strip().lower()
    if question_type_raw not in VALID_QUESTION_TYPES:
        raise ValueError(
            f"question_type inválido: '{question_type_raw}' (usa: {', '.join(sorted(VALID_QUESTION_TYPES))})"
        )

    prompt = (row.get("prompt") or "").strip()
    if not prompt:
        raise ValueError("prompt vacío")

    options: dict[str, str] = {}
    for letter in ("a", "b", "c", "d"):
        value = (row.get(f"option_{letter}") or "").strip()
        if not value:
            raise ValueError(f"option_{letter} vacía")
        options[letter.upper()] = value

    correct_answer = (row.get("correct_answer") or "").strip().upper()
    if correct_answer not in ("A", "B", "C", "D"):
        raise ValueError(f"correct_answer inválido: '{correct_answer}' (debe ser A, B, C o D)")

    passage_id = None
    passage_title = (row.get("passage_title") or "").strip()
    if passage_title:
        passage = passages_by_title.get(passage_title.lower())
        if passage is None:
            raise ValueError(f"no existe un passage con título '{passage_title}' (créalo primero)")
        passage_id = passage.id

    explanation = (row.get("explanation") or "").strip() or None

    return Question(
        section=Section(section_raw),
        question_type=QuestionType(question_type_raw),
        prompt=prompt,
        options=options,
        correct_answer=correct_answer,
        explanation=explanation,
        passage_id=passage_id,
        verified=True,
        source="Importado por CSV",
    )


def import_questions_from_csv(session: Session, teacher: User, file_bytes: bytes) -> tuple[int, list[dict]]:
    """
    Crea una pregunta por fila valida. Las filas invalidas NO detienen el
    import completo -- se reportan con su numero de fila y motivo exacto,
    para que el maestro pueda corregir solo esas y reintentar. utf-8-sig
    para tolerar el BOM que Excel agrega al exportar "CSV UTF-8".
    """
    try:
        text = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        return 0, [{"row": 0, "message": "El archivo no es un CSV de texto válido (usa codificación UTF-8)."}]

    reader = csv.DictReader(io.StringIO(text))
    fieldnames = set(reader.fieldnames or [])
    missing_columns = REQUIRED_CSV_COLUMNS - fieldnames
    if missing_columns:
        return 0, [{"row": 0, "message": f"Faltan columnas requeridas: {', '.join(sorted(missing_columns))}"}]

    passages_by_title = {p.title.strip().lower(): p for p in session.exec(select(Passage)).all() if p.title}

    created = 0
    errors: list[dict] = []

    for row_number, row in enumerate(reader, start=2):  # fila 1 es el encabezado
        try:
            question = _parse_csv_row(row, passages_by_title)
            question.source = f"Importado por {teacher.full_name}"
            session.add(question)
            session.commit()
            created += 1
        except Exception as exc:
            session.rollback()
            errors.append({"row": row_number, "message": str(exc)})

    return created, errors
