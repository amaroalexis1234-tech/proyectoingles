import uuid
from datetime import datetime

from sqlmodel import Field

from app.shared.base_model import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "users"

    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    full_name: str = Field(max_length=150)

    is_active: bool = Field(default=True)

    # "student" | "teacher". String simple (no Enum de SQLModel) para evitar
    # una migracion de tipo ENUM en MySQL si se agregan roles despues.
    # Se valida en el schema Pydantic de entrada, no aqui.
    role: str = Field(default="student", max_length=20)

    # Lectura rapida de XP sin agregar sobre xp_events en cada request.
    # La fuente de verdad sigue siendo xp_events (modulo progress);
    # este campo se recalcula/actualiza cuando se inserta un xp_event.
    current_xp: int = Field(default=0)

    # Ruta relativa servida por el mount de StaticFiles (ej. "/static/avatars/<id>.jpg").
    # El frontend le antepone el origen del backend para armar la URL completa.
    avatar_url: str | None = Field(default=None, max_length=255)


class PasswordResetToken(BaseModel, table=True):
    __tablename__ = "password_reset_tokens"

    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    token_hash: str = Field(unique=True, index=True, max_length=64)
    expires_at: datetime
    used: bool = Field(default=False)
