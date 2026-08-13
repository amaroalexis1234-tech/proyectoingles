import uuid
from datetime import date
from enum import Enum

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from app.shared.base_model import BaseModel


class XpReason(str, Enum):
    correct_answer = "correct_answer"
    mini_test_completed = "mini_test_completed"
    simulator_completed = "simulator_completed"
    daily_streak_bonus = "daily_streak_bonus"


class XpEvent(BaseModel, table=True):
    __tablename__ = "xp_events"

    # Fuente de verdad del XP (segun la arquitectura aprobada): nunca se
    # actualiza ni se borra un registro, solo se inserta. current_xp en
    # User es una cache de lectura rapida que se recalcula al insertar.
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    amount: int
    reason: XpReason


class StreakFreeze(BaseModel, table=True):
    """
    Un dia protegido explicitamente por el alumno (accion consciente, no
    automatica) para que una racha no se rompa por faltar ese dia -- igual
    que calculate_streak_days cuenta dias con XpEvent, tambien cuenta dias
    con un StreakFreeze. Limitado a uno por mes calendario (ver
    is_streak_freeze_available), nunca se otorgan de mas.
    """

    __tablename__ = "streak_freezes"

    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    date: date

    __table_args__ = (UniqueConstraint("user_id", "date", name="uq_streak_freeze_user_date"),)
