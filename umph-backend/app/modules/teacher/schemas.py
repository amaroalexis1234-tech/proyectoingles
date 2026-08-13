import uuid

from pydantic import BaseModel


class StudentSummary(BaseModel):
    id: uuid.UUID
    full_name: str
    email: str
    current_xp: int
    streak_days: int


class QuestionAnalytics(BaseModel):
    question_id: uuid.UUID
    section: str
    prompt: str
    attempts_count: int
    correct_count: int
    accuracy_percent: float


class QuestionAnalyticsResponse(BaseModel):
    questions: list[QuestionAnalytics]
    # Preguntas que nadie ha respondido todavia -- no se listan (no hay
    # precision real que mostrar) pero se cuentan para ser honestos sobre
    # que el banco tiene mas preguntas de las que aparecen aqui.
    untried_count: int
