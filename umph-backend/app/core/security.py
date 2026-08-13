from datetime import datetime, timedelta, timezone
from typing import Any, Literal
import hashlib
import secrets

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _create_token(subject: str, expires_delta: timedelta, token_type: Literal["access", "refresh"]) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,       # id del usuario
        "type": token_type,   # distingue access de refresh en el mismo decode
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(user_id: str) -> str:
    return _create_token(
        subject=user_id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


def create_refresh_token(user_id: str) -> str:
    return _create_token(
        subject=user_id,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
    )


def decode_token(token: str) -> dict[str, Any] | None:
    """Devuelve el payload si el token es valido, o None si expiro / fue manipulado."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None


def generate_password_reset_token() -> str:
    """
    Token aleatorio de alta entropia (no JWT) para recuperacion de contraseña.
    Se manda al usuario por email; solo su HASH se guarda en la base de datos,
    igual que hacemos con las contraseñas.
    """
    return secrets.token_urlsafe(32)


def hash_password_reset_token(raw_token: str) -> str:
    """
    SHA-256 en vez de bcrypt aqui: el token ya es aleatorio y de alta entropia
    (a diferencia de una contraseña elegida por el usuario), asi que no necesita
    un hash lento con salt; solo necesitamos poder buscarlo rapido por su hash.
    """
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
