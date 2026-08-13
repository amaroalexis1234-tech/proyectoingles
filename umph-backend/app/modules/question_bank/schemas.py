import uuid

from pydantic import BaseModel

from app.modules.question_bank.models import QuestionType, Section


class PassageCreate(BaseModel):
    title: str | None = None
    text: str
    source: str


class PassageRead(BaseModel):
    id: uuid.UUID
    title: str | None
    text: str
    source: str

    model_config = {"from_attributes": True}


class QuestionCreate(BaseModel):
    section: Section
    question_type: QuestionType
    prompt: str
    options: dict[str, str]
    correct_answer: str
    explanation: str | None = None
    passage_id: uuid.UUID | None = None


class QuestionUpdate(BaseModel):
    section: Section | None = None
    question_type: QuestionType | None = None
    prompt: str | None = None
    options: dict[str, str] | None = None
    correct_answer: str | None = None
    explanation: str | None = None
    passage_id: uuid.UUID | None = None


class QuestionRead(BaseModel):
    id: uuid.UUID
    section: Section
    question_type: QuestionType
    prompt: str
    options: dict
    correct_answer: str
    explanation: str | None
    passage_id: uuid.UUID | None
    verified: bool
    source: str

    model_config = {"from_attributes": True}


class QuestionImportError(BaseModel):
    row: int
    message: str


class QuestionImportResult(BaseModel):
    created: int
    errors: list[QuestionImportError]
