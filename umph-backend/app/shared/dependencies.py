from typing import Annotated

from fastapi import Depends, Header
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import decode_token
from app.modules.auth.models import User
from app.modules.auth.service import get_user_by_id
from app.shared.exceptions import InvalidOrExpiredTokenError, NotATeacherError

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(
    session: SessionDep,
    authorization: Annotated[str | None, Header()] = None,
) -> User:
    """
    Lee el access token del header 'Authorization: Bearer <token>',
    lo valida y devuelve el usuario autenticado.
    Se usa como Depends() en cualquier endpoint protegido.
    """
    if authorization is None or not authorization.startswith("Bearer "):
        raise InvalidOrExpiredTokenError()

    token = authorization.removeprefix("Bearer ")
    payload = decode_token(token)

    if payload is None or payload.get("type") != "access":
        raise InvalidOrExpiredTokenError()

    user = get_user_by_id(session, payload["sub"])
    if user is None or not user.is_active:
        raise InvalidOrExpiredTokenError()

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_current_teacher(current_user: CurrentUserDep) -> User:
    """
    Limite de seguridad real para todo endpoint de maestro -- el frontend
    solo refleja el rol, esto es lo que de verdad lo hace cumplir.
    """
    if current_user.role != "teacher":
        raise NotATeacherError()
    return current_user


CurrentTeacherDep = Annotated[User, Depends(get_current_teacher)]
