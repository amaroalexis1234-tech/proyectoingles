from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Raiz de umph-backend/ -- .../app/core/config.py -> app/core -> app -> raiz.
STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"


class Settings(BaseSettings):
    """
    Configuracion centralizada de la app.
    Todo valor sensible o dependiente de entorno vive aqui, nunca hardcodeado
    en el resto del codigo.
    """

    # --- App ---
    APP_NAME: str = "UPMH English Prep API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # --- Base de datos ---
    DATABASE_URL: str  # ej: mysql+pymysql://user:password@localhost:3306/umph_db

    # --- Seguridad / JWT ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- CORS ---
    FRONTEND_ORIGIN: str = "http://localhost:3000"

    # --- IA ---
    ANTHROPIC_API_KEY: str | None = None
    ANTHROPIC_MODEL: str = "claude-sonnet-5"

    # --- Email (recuperacion de contraseña) ---
    # Cualquier proveedor SMTP sirve (Gmail con App Password, Resend, SES, etc).
    # Sin configurar, request_password_reset cae en el fallback honesto ya
    # existente (token expuesto en la respuesta solo en development).
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM_EMAIL: str | None = None
    SMTP_FROM_NAME: str = "UPMH English Prep"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # se instancia una sola vez y se importa donde se necesite
