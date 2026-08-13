import uuid
from datetime import datetime

from pydantic import BaseModel

from app.modules.evaluations.models import MiniTestMode, TestType
from app.modules.learning.schemas import QuestionPublic


class StartMiniTestRequest(BaseModel):
    mode: MiniTestMode
    # Solo aplica a "grammar" y "mixed"; "reading" y "official" tienen
    # composicion fija y este valor se ignora si se manda.
    num_questions: int = 20


class PassageContext(BaseModel):
    id: uuid.UUID
    title: str | None
    text: str


class TestAttemptItemPublic(BaseModel):
    order_index: int
    question: QuestionPublic
    answered: bool
    # Se expone al reanudar para poder re-marcar la opcion ya elegida --
    # esto NO revela si fue correcta (eso sigue oculto en Simulador).
    selected_answer: str | None = None


class TestAttemptStarted(BaseModel):
    test_attempt_id: uuid.UUID
    test_type: TestType
    mini_test_mode: MiniTestMode | None
    total_questions: int
    time_limit_seconds: int | None
    started_at: datetime  # para calcular tiempo restante real al reanudar el Simulador
    items: list[TestAttemptItemPublic]
    passages: list[PassageContext]  # passages referenciados por las preguntas de reading incluidas


class SubmitTestAnswerRequest(BaseModel):
    question_id: uuid.UUID
    selected_answer: str


class SubmitTestAnswerResponse(BaseModel):
    # is_correct/correct_answer/explanation vienen en None durante el
    # Simulador (nunca se revela nada hasta el final, segun la arquitectura
    # aprobada). En Mini Test si se revelan de inmediato.
    recorded: bool
    is_correct: bool | None
    correct_answer: str | None
    explanation: str | None


class SectionScore(BaseModel):
    correct: int
    total: int


class TestResult(BaseModel):
    test_attempt_id: uuid.UUID
    total_questions: int
    correct_count: int
    accuracy: float
    section_scores: dict[str, SectionScore]
    xp_awarded: int
    started_at: datetime
    completed_at: datetime


class TestAttemptSummary(BaseModel):
    id: uuid.UUID
    test_type: TestType
    mini_test_mode: MiniTestMode | None
    completed_at: datetime | None
    total_questions: int
    correct_count: int
    accuracy: float


class InProgressAttempt(BaseModel):
    id: uuid.UUID
    test_type: TestType
    mini_test_mode: MiniTestMode | None
    total_questions: int
    answered_count: int
    started_at: datetime
