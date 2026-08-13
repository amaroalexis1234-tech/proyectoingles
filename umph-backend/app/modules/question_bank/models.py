import uuid
from enum import Enum

from sqlalchemy import JSON, Column, Text, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

from app.shared.base_model import BaseModel


class Section(str, Enum):
    structure = "structure"
    written_expression = "written_expression"
    reading = "reading"
    vocabulary = "vocabulary"


class QuestionType(str, Enum):
    sentence_completion = "sentence_completion"   # Structure: elegir la opcion que completa
    error_identification = "error_identification"  # Written Expression: elegir el segmento incorrecto
    multiple_choice = "multiple_choice"             # Reading: pregunta sobre un passage
    vocabulary_choice = "vocabulary_choice"         # Vocabulary: elegir el sinonimo/definicion correcta


class Skill(BaseModel, table=True):
    __tablename__ = "skills"

    # El PDF fuente usa catalogos de skill DISTINTOS por seccion (ej. Reading
    # tiene skills 1-13, Structure tiene skills 1-60 -- son numeraciones
    # independientes, no la misma escala). Por eso la unicidad es sobre
    # (section, number), nunca sobre number solo.
    section: Section
    number: int
    name: str | None = Field(default=None, max_length=200)

    __table_args__ = (UniqueConstraint("section", "number", name="uq_skill_section_number"),)


class QuestionSkillLink(SQLModel, table=True):
    __tablename__ = "question_skill_links"

    question_id: uuid.UUID = Field(foreign_key="questions.id", primary_key=True)
    skill_id: uuid.UUID = Field(foreign_key="skills.id", primary_key=True)


class Passage(BaseModel, table=True):
    __tablename__ = "passages"

    title: str | None = Field(default=None, max_length=200)
    text: str = Field(sa_column=Column(Text))  # texto completo del passage
    source: str = Field(max_length=200)  # ej. "TOEFL_tests_2026 - Exam 1 Reading Q1-9"


class Question(BaseModel, table=True):
    __tablename__ = "questions"

    section: Section
    question_type: QuestionType

    # Structure: la oracion con el hueco. Written Expression: la oracion
    # completa con los 4 segmentos subrayados marcados dentro del texto.
    # Reading: el enunciado de la pregunta (el passage vive aparte).
    prompt: str = Field(sa_column=Column(Text))

    # {"A": "...", "B": "...", "C": "...", "D": "..."}
    # Para written_expression, cada opcion es el segmento subrayado en si.
    options: dict = Field(sa_column=Column(JSON), default_factory=dict)

    correct_answer: str = Field(max_length=1)  # "A" | "B" | "C" | "D"

    # False = la respuesta fue determinada por analisis gramatical/lectura
    # (no copiada de un answer key oficial del libro, porque esa pagina
    # no se extrajo). True = confirmada contra el answer key real.
    verified: bool = Field(default=False)

    explanation: str | None = Field(default=None, sa_column=Column(Text))  # por que es correcta

    passage_id: uuid.UUID | None = Field(default=None, foreign_key="passages.id")
    source: str = Field(max_length=200)  # ej. "TOEFL_tests_2026 - Exam 1 Structure Q1-15"

    skills: list[Skill] = Relationship(link_model=QuestionSkillLink)
