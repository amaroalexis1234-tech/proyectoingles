from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.core.config import settings

# pool_pre_ping evita errores de "MySQL server has gone away" en conexiones
# que estuvieron inactivas por mucho tiempo (comun en MySQL).
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG, pool_pre_ping=True)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency de FastAPI: entrega una sesion por request y la cierra al final,
    incluso si ocurre una excepcion.
    """
    with Session(engine) as session:
        yield session
