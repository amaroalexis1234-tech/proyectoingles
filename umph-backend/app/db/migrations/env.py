from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlmodel import SQLModel

from alembic import context

# Import explicito de cada modulo con modelos: SQLModel solo registra una
# tabla en su metadata cuando el archivo que la define fue importado.
# Cuando agreguemos modules/learning, evaluations, etc. con sus propios
# models.py, se agregan aqui tambien.
from app.core.config import settings
from app.modules.auth.models import User, PasswordResetToken  # noqa: F401
from app.modules.question_bank.models import Skill, Passage, Question, QuestionSkillLink  # noqa: F401
from app.modules.progress.models import XpEvent, StreakFreeze  # noqa: F401
from app.modules.learning.models import ExerciseAttempt  # noqa: F401
from app.modules.evaluations.models import TestAttempt, TestAttemptItem  # noqa: F401
from app.modules.ai.models import AiExplanationCache  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# La URL de conexion viene de nuestro Settings (.env), nunca de alembic.ini,
# para no tener credenciales duplicadas en dos archivos distintos.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
