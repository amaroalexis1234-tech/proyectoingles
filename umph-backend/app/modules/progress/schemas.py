from pydantic import BaseModel


class WeakSkill(BaseModel):
    """
    Placeholder tipado: hasta que exista Learning (que genera intentos
    reales por skill), el Dashboard no tiene datos para calcular esto.
    El shape ya queda listo para cuando sí los haya.
    """

    skill_number: int
    section: str
    accuracy: float


class QuickPracticeSuggestion(BaseModel):
    section: str
    reason: str


class LevelEstimate(BaseModel):
    """Aproximacion basada en accuracy real sobre evaluaciones completadas -- ver level_estimation.py."""

    estimated_score: int
    cefr_band: str
    band_progress_percent: float
    based_on_attempts: int


class XpLevel(BaseModel):
    """Nivel de gamificacion por XP -- concepto distinto de LevelEstimate (ese es de dominio del examen)."""

    level: int
    current_xp_in_level: int
    xp_for_next_level: int


class DailyGoal(BaseModel):
    target_count: int
    completed_count: int
    completed: bool


class StudyStatistics(BaseModel):
    questions_answered: int
    accuracy_percent: float | None  # None (no 0.0) cuando no hay ningun dato todavia
    study_time_seconds: int
    completed_simulators: int
    completed_mini_tests: int
    day_streak: int
    correct_count: int
    incorrect_count: int
    # TestAttemptItem.selected_answer aun nulo en intentos YA completados
    # (se puede terminar una evaluacion sin responder todo).
    unanswered_count: int


class WeeklyEvolutionDay(BaseModel):
    day_label: str  # "Lun".."Dom"
    accuracy_percent: float | None  # None = sin actividad ese dia (incluye dias futuros de la semana en curso)


class DashboardSummary(BaseModel):
    current_xp: int
    streak_days: int
    weak_skills: list[WeakSkill]
    quick_practice: list[QuickPracticeSuggestion]
    has_enough_data_for_recommendations: bool
    xp_level: XpLevel
    level: LevelEstimate | None
    has_enough_data_for_level: bool
    daily_goal: DailyGoal
    streak_freeze_available: bool
