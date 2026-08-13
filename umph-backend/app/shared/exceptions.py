class DomainError(Exception):
    """Excepcion base para errores de negocio (no de infraestructura)."""


class EmailAlreadyExistsError(DomainError):
    def __init__(self) -> None:
        super().__init__("Ya existe una cuenta registrada con este correo.")


class InvalidCredentialsError(DomainError):
    def __init__(self) -> None:
        super().__init__("Correo o contraseña incorrectos.")


class InvalidOrExpiredTokenError(DomainError):
    def __init__(self) -> None:
        super().__init__("La sesión expiró o el token no es válido.")


class UserNotFoundError(DomainError):
    def __init__(self) -> None:
        super().__init__("Usuario no encontrado.")


class NotATeacherError(DomainError):
    def __init__(self) -> None:
        super().__init__("Esta acción requiere una cuenta de maestro.")


class InvalidAvatarFileError(DomainError):
    def __init__(self) -> None:
        super().__init__("El archivo debe ser una imagen JPG, PNG, WEBP o GIF de máximo 5 MB.")
