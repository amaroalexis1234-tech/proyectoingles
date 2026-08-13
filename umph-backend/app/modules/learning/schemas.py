import uuid

from pydantic import BaseModel


class QuestionPublic(BaseModel):
    """
    Version publica de una pregunta: nunca incluye correct_answer ni
    explanation antes de que el estudiante responda -- eso solo se
    revela en la respuesta de POST /learning/attempts.
    """

    id: uuid.UUID
    section: str
    question_type: str
    prompt: str
    options: dict
    passage_id: uuid.UUID | None = None

    model_config = {"from_attributes": True}


class PassageWithQuestions(BaseModel):
    passage_id: uuid.UUID
    title: str | None
    text: str
    questions: list[QuestionPublic]


class PassageSummary(BaseModel):
    id: uuid.UUID
    title: str | None

    model_config = {"from_attributes": True}


class SubmitAttemptRequest(BaseModel):
    question_id: uuid.UUID
    selected_answer: str
    time_spent_seconds: int | None = None


class SubmitAttemptResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str | None
    xp_awarded: int
