import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    """
    Mixin comun para todas las entidades persistentes.
    UUID como PK (en vez de autoincrement) para no exponer conteos de
    registros ni facilitar enumeracion de IDs desde el frontend.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
