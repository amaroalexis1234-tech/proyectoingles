import uuid

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=150)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    current_xp: int
    role: str
    avatar_url: str | None

    model_config = {"from_attributes": True}  # permite construir desde el modelo SQLModel


class AccessTokenResponse(BaseModel):
    """
    Solo el access token viaja en el body de la respuesta.
    El refresh token se setea como cookie httpOnly desde el router
    y nunca es visible/legible por JavaScript en el frontend.
    """

    access_token: str
    token_type: str = "bearer"
    user: UserRead


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    message: str
    # Solo se llena en ENVIRONMENT=development, como stopgap mientras no
    # exista un servicio de email real conectado. En produccion siempre None.
    dev_reset_token: str | None = None


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class UpdateProfileRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)
