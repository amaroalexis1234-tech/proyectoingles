import uuid

from pydantic import BaseModel


class ExplainQuestionRequest(BaseModel):
    question_id: uuid.UUID
    # La opcion que eligio el estudiante, para que la explicacion pueda
    # comentar especificamente por que esa opcion esta mal (si aplica).
    student_answer: str | None = None


class VocabularyTerm(BaseModel):
    term: str
    translation: str


class ExplanationPayload(BaseModel):
    """
    Shape exacto pedido a Claude via tool use forzado, y el mismo shape que
    debe poblar el camino de fallback (solo explanation, el resto None) --
    nunca se fabrica evidencia/vocabulario/regla/traduccion.
    """

    explanation: str
    evidence: str | None = None
    vocabulary_terms: list[VocabularyTerm] | None = None
    grammar_rule: str | None = None
    translation: str | None = None


class ExplainQuestionResponse(ExplanationPayload):
    # "ai" = generado en vivo por Claude. "fallback" = no hay ANTHROPIC_API_KEY
    # configurada o la llamada fallo, se uso la explicacion pre-guardada de
    # la pregunta (si existe) o un mensaje generico.
    source: str


class RecommendPracticeRequest(BaseModel):
    attempt_id: uuid.UUID


class RecommendationResponse(BaseModel):
    recommendation: str
    # "ai" = generado en vivo por Claude. "fallback" = calculado deterministicamente
    # a partir de section_scores (sigue siendo un dato real, no un mensaje
    # generico) cuando no hay API key o la llamada falla.
    source: str
