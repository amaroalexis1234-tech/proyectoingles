import uuid
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.core.config import STATIC_DIR, settings
from app.core.email import send_email
from app.core.security import (
    generate_password_reset_token,
    hash_password,
    hash_password_reset_token,
    verify_password,
)
from app.modules.auth.models import PasswordResetToken, User
from app.modules.auth.schemas import RegisterRequest
from app.shared.exceptions import (
    EmailAlreadyExistsError,
    InvalidAvatarFileError,
    InvalidCredentialsError,
    InvalidOrExpiredTokenError,
)

PASSWORD_RESET_TOKEN_TTL_MINUTES = 30

_RESET_EMAIL_TEXT = (
    "Hola {name},\n\n"
    "Recibimos una solicitud para restablecer tu contraseña de UPMH English Prep.\n\n"
    "Abre este enlace para elegir una nueva contraseña (expira en {ttl} minutos):\n{url}\n\n"
    "Si tú no pediste esto, puedes ignorar este correo."
)

_RESET_EMAIL_HTML = (
    "<p>Hola {name},</p>"
    "<p>Recibimos una solicitud para restablecer tu contraseña de <strong>UPMH English Prep</strong>.</p>"
    '<p><a href="{url}">Haz clic aquí para elegir una nueva contraseña</a> '
    "(el enlace expira en {ttl} minutos).</p>"
    "<p>Si tú no pediste esto, puedes ignorar este correo.</p>"
)

AVATAR_EXTENSION_BY_CONTENT_TYPE = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}
MAX_AVATAR_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def register_user(session: Session, data: RegisterRequest) -> User:
    existing = session.exec(select(User).where(User.email == data.email)).first()
    if existing is not None:
        raise EmailAlreadyExistsError()

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> User:
    user = session.exec(select(User).where(User.email == email)).first()
    if user is None or not verify_password(password, user.hashed_password):
        # Mensaje identico si el correo no existe o la contraseña es incorrecta:
        # no revelamos cual de las dos cosas fallo (evita enumeracion de emails).
        raise InvalidCredentialsError()
    return user


def get_user_by_id(session: Session, user_id: str) -> User | None:
    # El "sub" del JWT siempre es str; la PK en el modelo es uuid.UUID,
    # asi que hay que convertir explicitamente antes de consultar.
    try:
        parsed_id = uuid.UUID(user_id)
    except ValueError:
        return None
    return session.get(User, parsed_id)


def request_password_reset(session: Session, email: str) -> tuple[bool, str | None]:
    """
    Si el email existe, crea un token de reset y trata de enviarlo por correo
    real via SMTP. Devuelve (email_enviado, token_crudo) -- el router solo
    expone el token en la respuesta cuando el envio fallo o no hay SMTP
    configurado (fallback honesto para poder seguir probando el flujo sin
    bandeja de entrada real), nunca cuando el correo si se mando.
    Si el email NO existe, devuelve (False, None) silenciosamente: el router
    siempre responde el mismo mensaje generico (evita enumeracion de emails).
    """
    user = session.exec(select(User).where(User.email == email)).first()
    if user is None:
        return False, None

    raw_token = generate_password_reset_token()
    reset_token = PasswordResetToken(
        user_id=user.id,
        token_hash=hash_password_reset_token(raw_token),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=PASSWORD_RESET_TOKEN_TTL_MINUTES),
    )
    session.add(reset_token)
    session.commit()

    reset_url = f"{settings.FRONTEND_ORIGIN}/reset-password?token={raw_token}"
    email_sent = send_email(
        to_email=user.email,
        subject="Restablece tu contraseña — UPMH English Prep",
        html_body=_RESET_EMAIL_HTML.format(
            name=user.full_name, url=reset_url, ttl=PASSWORD_RESET_TOKEN_TTL_MINUTES
        ),
        text_body=_RESET_EMAIL_TEXT.format(
            name=user.full_name, url=reset_url, ttl=PASSWORD_RESET_TOKEN_TTL_MINUTES
        ),
    )
    return email_sent, raw_token


def update_profile(session: Session, user: User, full_name: str) -> User:
    user.full_name = full_name
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_avatar(session: Session, user: User, content_type: str | None, file_bytes: bytes) -> User:
    extension = AVATAR_EXTENSION_BY_CONTENT_TYPE.get(content_type or "")
    if extension is None:
        raise InvalidAvatarFileError()
    if len(file_bytes) > MAX_AVATAR_SIZE_BYTES:
        raise InvalidAvatarFileError()

    avatars_dir = STATIC_DIR / "avatars"
    avatars_dir.mkdir(parents=True, exist_ok=True)

    # Un archivo por usuario, sobrescrito en cada subida -- el nombre viene
    # del id del usuario (nunca del nombre original del archivo, evita
    # problemas de path traversal / colisiones).
    filename = f"{user.id}{extension}"
    (avatars_dir / filename).write_bytes(file_bytes)

    user.avatar_url = f"/static/avatars/{filename}"
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def change_password(session: Session, user: User, current_password: str, new_password: str) -> None:
    if not verify_password(current_password, user.hashed_password):
        # Mismo error que login: no da pistas de si el problema es la
        # contraseña actual especificamente.
        raise InvalidCredentialsError()

    user.hashed_password = hash_password(new_password)
    session.add(user)
    session.commit()


def reset_password(session: Session, raw_token: str, new_password: str) -> None:
    token_hash = hash_password_reset_token(raw_token)
    reset_token = session.exec(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
    ).first()

    now = datetime.now(timezone.utc)
    is_valid = (
        reset_token is not None
        and not reset_token.used
        and reset_token.expires_at.replace(tzinfo=timezone.utc) > now
    )
    if not is_valid:
        raise InvalidOrExpiredTokenError()

    user = session.get(User, reset_token.user_id)
    if user is None:
        raise InvalidOrExpiredTokenError()

    user.hashed_password = hash_password(new_password)
    reset_token.used = True
    session.add(user)
    session.add(reset_token)
    session.commit()
