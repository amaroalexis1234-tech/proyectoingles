"""add vocabulary section and vocabulary_choice type

Revision ID: fbbf65e83d2f
Revises: 72b47225ec24
Create Date: 2026-08-09 06:13:45.816235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'fbbf65e83d2f'
down_revision: Union[str, None] = '72b47225ec24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite no tiene ENUM nativo (la columna ya es texto libre, no
    # requiere cambios). MySQL si define un ENUM real a nivel de columna,
    # asi que hay que ampliarlo explicitamente para aceptar los nuevos
    # valores 'vocabulary' y 'vocabulary_choice'.
    bind = op.get_bind()
    if bind.dialect.name == "mysql":
        op.alter_column(
            "questions",
            "section",
            existing_type=sa.Enum("structure", "written_expression", "reading", name="section"),
            type_=sa.Enum("structure", "written_expression", "reading", "vocabulary", name="section"),
            existing_nullable=False,
        )
        op.alter_column(
            "questions",
            "question_type",
            existing_type=sa.Enum(
                "sentence_completion", "error_identification", "multiple_choice", name="questiontype"
            ),
            type_=sa.Enum(
                "sentence_completion",
                "error_identification",
                "multiple_choice",
                "vocabulary_choice",
                name="questiontype",
            ),
            existing_nullable=False,
        )
        op.alter_column(
            "skills",
            "section",
            existing_type=sa.Enum("structure", "written_expression", "reading", name="section"),
            type_=sa.Enum("structure", "written_expression", "reading", "vocabulary", name="section"),
            existing_nullable=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "mysql":
        op.alter_column(
            "skills",
            "section",
            existing_type=sa.Enum("structure", "written_expression", "reading", "vocabulary", name="section"),
            type_=sa.Enum("structure", "written_expression", "reading", name="section"),
            existing_nullable=False,
        )
        op.alter_column(
            "questions",
            "question_type",
            existing_type=sa.Enum(
                "sentence_completion",
                "error_identification",
                "multiple_choice",
                "vocabulary_choice",
                name="questiontype",
            ),
            type_=sa.Enum(
                "sentence_completion", "error_identification", "multiple_choice", name="questiontype"
            ),
            existing_nullable=False,
        )
        op.alter_column(
            "questions",
            "section",
            existing_type=sa.Enum("structure", "written_expression", "reading", "vocabulary", name="section"),
            type_=sa.Enum("structure", "written_expression", "reading", name="section"),
            existing_nullable=False,
        )
