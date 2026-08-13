import uuid

from sqlmodel import Field

from app.shared.base_model import BaseModel


class ExerciseAttempt(BaseModel, table=True):
    __tablename__ = "exercise_attempts"

    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    question_id: uuid.UUID = Field(foreign_key="questions.id", index=True)

    selected_answer: str = Field(max_length=1)  # "A" | "B" | "C" | "D"
    is_correct: bool
    time_spent_seconds: int | None = Field(default=None)
