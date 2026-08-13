import uuid

from sqlalchemy import JSON, Column, UniqueConstraint
from sqlmodel import Field

from app.shared.base_model import BaseModel


class AiExplanationCache(BaseModel, table=True):
    """
    Una explicacion de Claude por (pregunta, respuesta del alumno) -- se
    reusa entre alumnos y entre intentos en vez de pagar una llamada nueva
    cada vez que alguien pide la misma explicacion. La respuesta SI depende
    de student_answer (el prompt explica por que esa opcion especifica esta
    mal), por eso la cache no es solo por pregunta.
    """

    __tablename__ = "ai_explanation_cache"

    question_id: uuid.UUID = Field(foreign_key="questions.id", index=True)
    # "" (no NULL) cuando se pidio la explicacion sin respuesta del alumno --
    # asi la unique constraint funciona igual en MySQL (NULL no es comparable
    # consigo mismo en un UNIQUE).
    student_answer: str = Field(default="", max_length=1)
    payload: dict = Field(sa_column=Column(JSON))

    __table_args__ = (UniqueConstraint("question_id", "student_answer", name="uq_ai_cache_question_answer"),)
