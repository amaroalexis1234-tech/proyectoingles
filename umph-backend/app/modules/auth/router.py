from typing import Annotated

from fastapi import APIRouter, Cookie, File, Response, UploadFile, status

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.modules.auth.schemas import (
    AccessTokenResponse,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    UpdateProfileRequest,
    UserRead,
)
from app.modules.auth.service import (
    authenticate_user,
    change_password,
    get_user_by_id,
    register_user,
    request_password_reset,
    reset_password,
    update_avatar,
    update_profile,
)
from app.shared.dependencies import CurrentUserDep, SessionDep
from app.shared.exceptions import InvalidOrExpiredTokenError

router = APIRouter(prefix="/auth", tags=["auth"])

REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_MAX_AGE = 60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS


def _set_refresh_cookie(response: Response, user_id: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=create_refresh_token(user_id),
        httponly=True,
        secure=settings.ENVIRONMENT != "development",  # requiere HTTPS en produccion
        samesite="lax",
        max_age=REFRESH_COOKIE_MAX_AGE,
        # Debe coincidir con el prefijo real montado en main.py (app.include_router(..., prefix="/api")).
        # Si difieren, el navegador nunca envia la cookie de vuelta.
        path="/api/auth",
    )


@router.post("/register", response_model=AccessTokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, session: SessionDep, response: Response) -> AccessTokenResponse:
    user = register_user(session, data)
    _set_refresh_cookie(response, str(user.id))
    return AccessTokenResponse(access_token=create_access_token(str(user.id)), user=UserRead.model_validate(user))


@router.post("/login", response_model=AccessTokenResponse)
def login(data: LoginRequest, session: SessionDep, response: Response) -> AccessTokenResponse:
    user = authenticate_user(session, data.email, data.password)
    _set_refresh_cookie(response, str(user.id))
    return AccessTokenResponse(access_token=create_access_token(str(user.id)), user=UserRead.model_validate(user))


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(
    session: SessionDep,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> AccessTokenResponse:
    """
    Lee el refresh token directamente de la cookie httpOnly (el frontend nunca
    lo manda a mano). Si es valido, rota ambos tokens: emite un access token
    nuevo y tambien un refresh token nuevo (rotacion), reduciendo la ventana
    de uso si un refresh token llegara a filtrarse.
    """
    if refresh_token is None:
        raise InvalidOrExpiredTokenError()

    payload = decode_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise InvalidOrExpiredTokenError()

    user = get_user_by_id(session, payload["sub"])
    if user is None or not user.is_active:
        raise InvalidOrExpiredTokenError()

    _set_refresh_cookie(response, str(user.id))
    return AccessTokenResponse(access_token=create_access_token(str(user.id)), user=UserRead.model_validate(user))


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: CurrentUserDep) -> UserRead:
    return UserRead.model_validate(current_user)


@router.patch("/me", response_model=UserRead)
def update_current_user(
    data: UpdateProfileRequest, session: SessionDep, current_user: CurrentUserDep
) -> UserRead:
    updated_user = update_profile(session, current_user, data.full_name)
    return UserRead.model_validate(updated_user)


@router.post("/me/avatar", response_model=UserRead)
async def upload_avatar(
    session: SessionDep, current_user: CurrentUserDep, file: UploadFile = File(...)
) -> UserRead:
    file_bytes = await file.read()
    updated_user = update_avatar(session, current_user, file.content_type, file_bytes)
    return UserRead.model_validate(updated_user)


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password_endpoint(
    data: ChangePasswordRequest, session: SessionDep, current_user: CurrentUserDep
) -> None:
    change_password(session, current_user, data.current_password, data.new_password)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> None:
    response.delete_cookie(key=REFRESH_COOKIE_NAME, path="/api/auth")


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(data: ForgotPasswordRequest, session: SessionDep) -> ForgotPasswordResponse:
    email_sent, raw_token = request_password_reset(session, data.email)

    # Mensaje identico exista o no el email: evita que alguien use este
    # endpoint para descubrir que correos estan registrados.
    generic_message = "Si el correo existe, recibirás un enlace para restablecer tu contraseña."

    # El token solo se expone en la respuesta cuando el correo NO se pudo
    # enviar de verdad (SMTP sin configurar o fallo) y estamos en desarrollo --
    # es el fallback para poder seguir probando el flujo sin bandeja de entrada.
    dev_token = raw_token if (not email_sent and settings.ENVIRONMENT == "development" and raw_token) else None

    return ForgotPasswordResponse(message=generic_message, dev_reset_token=dev_token)


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
def reset_password_endpoint(data: ResetPasswordRequest, session: SessionDep) -> None:
    reset_password(session, data.token, data.new_password)
