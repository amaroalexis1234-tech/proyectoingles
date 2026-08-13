
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import STATIC_DIR, settings
from app.modules.auth.router import router as auth_router
from app.modules.learning.router import router as learning_router
from app.modules.progress.router import router as progress_router
from app.shared.exceptions import (
    DomainError,
    EmailAlreadyExistsError,
    InvalidAvatarFileError,
    InvalidCredentialsError,
    InvalidOrExpiredTokenError,
    NotATeacherError,
    UserNotFoundError,
)
from app.modules.learning.service import (
    InvalidSectionForExercisesError,
    QuestionNotFoundError,
)
from app.modules.evaluations.router import router as evaluations_router
from app.modules.evaluations.service import (
    QuestionNotInAttemptError,
    TestAttemptAlreadyCompletedError,
    TestAttemptNotFoundError,
    TestAttemptNotOwnedError,
)
from app.modules.ai.router import router as ai_router
from app.modules.ai.service import (
    QuestionNotFoundError as AiQuestionNotFoundError,
)
from app.modules.question_bank.router import router as question_bank_router
from app.modules.question_bank.service import (
    PassageNotFoundError,
    QuestionNotFoundError as QuestionBankQuestionNotFoundError,
)
from app.modules.progress.service import NoActiveStreakError, StreakAlreadyActiveError, StreakFreezeAlreadyUsedError
from app.modules.teacher.router import router as teacher_router

app = FastAPI(title=settings.APP_NAME)


# --- CORS ---
# localhost/127.0.0.1 siempre permitidos (desarrollo). settings.FRONTEND_ORIGIN
# se agrega aparte -- en produccion apunta al dominio real del frontend
# desplegado (ej. Vercel), configurable sin tocar codigo.

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(
        dict.fromkeys(
            [
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                settings.FRONTEND_ORIGIN,
            ]
        )
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Traducción de errores de dominio a códigos HTTP ---

# Un solo lugar decide "EmailAlreadyExistsError -> 409",
# en vez de que cada router tenga que saber de status codes HTTP.

_DOMAIN_ERROR_STATUS: dict[type[DomainError], int] = {
    EmailAlreadyExistsError: status.HTTP_409_CONFLICT,
    InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,
    InvalidOrExpiredTokenError: status.HTTP_401_UNAUTHORIZED,
    QuestionNotFoundError: status.HTTP_404_NOT_FOUND,
    InvalidSectionForExercisesError: status.HTTP_400_BAD_REQUEST,
    TestAttemptNotFoundError: status.HTTP_404_NOT_FOUND,
    TestAttemptNotOwnedError: status.HTTP_403_FORBIDDEN,
    TestAttemptAlreadyCompletedError: status.HTTP_409_CONFLICT,
    QuestionNotInAttemptError: status.HTTP_400_BAD_REQUEST,
    AiQuestionNotFoundError: status.HTTP_404_NOT_FOUND,
    NotATeacherError: status.HTTP_403_FORBIDDEN,
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    QuestionBankQuestionNotFoundError: status.HTTP_404_NOT_FOUND,
    PassageNotFoundError: status.HTTP_404_NOT_FOUND,
    InvalidAvatarFileError: status.HTTP_400_BAD_REQUEST,
    StreakFreezeAlreadyUsedError: status.HTTP_409_CONFLICT,
    StreakAlreadyActiveError: status.HTTP_409_CONFLICT,
    NoActiveStreakError: status.HTTP_409_CONFLICT,
}


@app.exception_handler(DomainError)
def handle_domain_error(
    request: Request,
    exc: DomainError,
) -> JSONResponse:
    status_code = _DOMAIN_ERROR_STATUS.get(
        type(exc),
        status.HTTP_400_BAD_REQUEST,
    )

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )


# --- Routers ---

app.include_router(auth_router, prefix="/api")
app.include_router(progress_router, prefix="/api")
app.include_router(learning_router, prefix="/api")
app.include_router(evaluations_router, prefix="/api")
app.include_router(ai_router, prefix="/api")
app.include_router(question_bank_router, prefix="/api")
app.include_router(teacher_router, prefix="/api")


# --- Archivos estaticos (avatares subidos por usuarios) ---
# Fuera del prefijo /api a proposito: son archivos, no endpoints de la API.
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# --- Health check ---

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
