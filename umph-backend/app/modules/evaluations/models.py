import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Column, Text
from sqlmodel import Field

from app.shared.base_model import BaseModel


class TestType(str, Enum):
    mini_test = "mini_test"
    simulator = "simulator"


class MiniTestMode(str, Enum):
    grammar = "grammar"      # Structure + Written Expression
    reading = "reading"      # un passage completo
    mixed = "mixed"          # Grammar + Vocabulary
    official = "official"    # muestra fija de las 4 secciones


class TestAttempt(BaseModel, table=True):
    __tablename__ = "test_attempts"

    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    test_type: TestType
    mini_test_mode: MiniTestMode | None = Field(default=None)

    started_at: datetime
    completed_at: datetime | None = Field(default=None)

    total_questions: int
    correct_count: int = Field(default=0)

    # {"structure": {"correct": 8, "total": 15}, "written_expression": {...}, ...}
    section_scores: dict = Field(sa_column=Column(JSON), default_factory=dict)

    # Cache de la recomendacion de Claude para este intento -- section_scores
    # ya no cambia una vez completado, asi que se genera una sola vez y se
    # reusa en cada visita a la pantalla de resultados en vez de pagar una
    # llamada nueva cada vez.
    ai_recommendation: str | None = Field(default=None, sa_column=Column(Text))


class TestAttemptItem(BaseModel, table=True):
    """
    Una fila por cada pregunta que forma parte de un TestAttempt, en el
    orden en que se presenta. Se crea vacia (selected_answer=None) al
    armar el test, y se completa a medida que el estudiante responde --
    asi el simulador puede reanudarse si se recarga la pagina a medio camino.
    """

    __tablename__ = "test_attempt_items"

    test_attempt_id: uuid.UUID = Field(foreign_key="test_attempts.id", index=True)
    question_id: uuid.UUID = Field(foreign_key="questions.id")
    order_index: int

    selected_answer: str | None = Field(default=None, max_length=1)
    is_correct: bool | None = Field(default=None)
    # Null en filas viejas (nunca se respondieron o se crearon antes de este
    # campo) -- se excluyen correctamente de conteos "de hoy", no se infieren.
    answered_at: datetime | None = Field(default=None)
