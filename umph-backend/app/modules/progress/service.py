import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlmodel import Session, select

from app.modules.auth.models import User
from app.modules.evaluations.models import TestAttempt, TestAttemptItem, TestType
from app.modules.learning.models import ExerciseAttempt
from app.modules.progress.level_estimation import cefr_band_for_score, score_from_accuracy
from app.modules.progress.models import StreakFreeze, XpEvent, XpReason
from app.modules.progress.schemas import (
    DailyGoal,
    DashboardSummary,
    LevelEstimate,
    QuickPracticeSuggestion,
    StudyStatistics,
    WeakSkill,
    WeeklyEvolutionDay,
    XpLevel,
)
from app.modules.question_bank.models import Question
from app.shared.exceptions import DomainError

class StreakFreezeAlreadyUsedError(DomainError):
    def __init__(self) -> None:
        super().__init__("Ya usaste tu congelamiento de racha este mes. Vuelve a estar disponible el próximo mes.")


class StreakAlreadyActiveError(DomainError):
    def __init__(self) -> None:
        super().__init__("Ya tienes actividad hoy, no necesitas congelar tu racha.")


class NoActiveStreakError(DomainError):
    def __init__(self) -> None:
        super().__init__("No tienes una racha activa que proteger todavía.")


MIN_ATTEMPTS_PER_SKILL = 3
MIN_TOTAL_ATTEMPTS_FOR_RECOMMENDATIONS = 5
WEAK_ACCURACY_THRESHOLD = 0.7
ALL_SECTIONS = ["structure", "written_expression", "reading", "vocabulary"]

MIN_COMPLETED_EVALUATIONS_FOR_LEVEL = 3
XP_PER_LEVEL = 2000  # decision de producto, ajustable
DAILY_GOAL_TARGET_QUESTIONS = 20  # regla fija, no configurable por el usuario
WEEKDAY_LABELS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]


def _collect_answer_records(session: Session, user_id: uuid.UUID) -> list[tuple[uuid.UUID, bool]]:
    """
    Junta TODOS los intentos de respuesta del usuario, vengan de Learning
    (practica suelta) o de Evaluations (mini tests / simulador). Ambas
    fuentes cuentan igual para calcular en que necesita reforzar.
    """
    exercise_records = session.exec(
        select(ExerciseAttempt.question_id, ExerciseAttempt.is_correct).where(
            ExerciseAttempt.user_id == user_id
        )
    ).all()

    test_records = session.exec(
        select(TestAttemptItem.question_id, TestAttemptItem.is_correct)
        .join(TestAttempt, TestAttempt.id == TestAttemptItem.test_attempt_id)
        .where(TestAttempt.user_id == user_id, TestAttemptItem.is_correct.is_not(None))
    ).all()

    return list(exercise_records) + list(test_records)


def calculate_weak_skills(session: Session, user_id: uuid.UUID) -> list[WeakSkill]:
    records = _collect_answer_records(session, user_id)

    skill_stats: dict[tuple[str, int], list[int]] = {}
    for question_id, is_correct in records:
        question = session.get(Question, question_id)
        if question is None:
            continue
        for skill in question.skills:
            key = (skill.section.value, skill.number)
            stats = skill_stats.setdefault(key, [0, 0])  # [correctas, total]
            stats[1] += 1
            if is_correct:
                stats[0] += 1

    weak_skills = []
    for (section, number), (correct, total) in skill_stats.items():
        if total < MIN_ATTEMPTS_PER_SKILL:
            continue  # muy pocos datos para sacar una conclusion confiable
        accuracy = correct / total
        if accuracy < WEAK_ACCURACY_THRESHOLD:
            weak_skills.append(WeakSkill(skill_number=number, section=section, accuracy=round(accuracy * 100, 1)))

    weak_skills.sort(key=lambda w: w.accuracy)
    return weak_skills[:5]


def calculate_quick_practice(session: Session, user_id: uuid.UUID) -> list[QuickPracticeSuggestion]:
    records = _collect_answer_records(session, user_id)

    section_stats: dict[str, list[int]] = {}
    for question_id, is_correct in records:
        question = session.get(Question, question_id)
        if question is None:
            continue
        stats = section_stats.setdefault(question.section.value, [0, 0])
        stats[1] += 1
        if is_correct:
            stats[0] += 1

    suggestions = []
    for section in ALL_SECTIONS:
        correct, total = section_stats.get(section, (0, 0))
        if total == 0:
            suggestions.append(QuickPracticeSuggestion(section=section, reason="Todavía no has practicado esta sección."))
        else:
            accuracy = correct / total
            if accuracy < WEAK_ACCURACY_THRESHOLD:
                suggestions.append(
                    QuickPracticeSuggestion(
                        section=section, reason=f"Tu precisión aquí es {round(accuracy * 100)}% — vale la pena reforzar."
                    )
                )

    return suggestions[:3]


def record_xp_event(session: Session, user: User, amount: int, reason: XpReason) -> XpEvent:
    """
    Unica forma de otorgar XP en todo el sistema: inserta el evento
    (fuente de verdad) y actualiza el cache de lectura rapida en User.
    La usaran Learning y Evaluations mas adelante, nunca escriben
    directo a current_xp.
    """
    event = XpEvent(user_id=user.id, amount=amount, reason=reason)
    session.add(event)

    user.current_xp += amount
    session.add(user)

    session.commit()
    session.refresh(event)
    return event


def calculate_streak_days(session: Session, user_id: uuid.UUID) -> int:
    """
    Racha de dias consecutivos con al menos un evento de XP -- o un dia
    protegido explicitamente con un StreakFreeze (ver activate_streak_freeze),
    que cuenta igual que un dia con actividad real -- contando hacia atras
    desde hoy. Si el ultimo dia con actividad/freeze fue anteayer o antes,
    la racha esta rota y se devuelve 0.
    """
    xp_rows = session.exec(select(XpEvent.created_at).where(XpEvent.user_id == user_id)).all()
    freeze_rows = session.exec(select(StreakFreeze.date).where(StreakFreeze.user_id == user_id)).all()
    if not xp_rows and not freeze_rows:
        return 0

    # UTC, no hora local del servidor -- created_at se guarda en UTC
    # (BaseModel), comparar contra date.today() (local) desalinea "hoy"
    # hasta por varias horas segun el huso horario del servidor.
    activity_dates = {ts.date() for ts in xp_rows} | set(freeze_rows)
    unique_dates = sorted(activity_dates, reverse=True)
    today = datetime.now(timezone.utc).date()

    # Si no hay actividad hoy NI ayer, la racha ya se rompio.
    if unique_dates[0] < today - timedelta(days=1):
        return 0

    streak = 1
    for i in range(1, len(unique_dates)):
        if unique_dates[i - 1] - unique_dates[i] == timedelta(days=1):
            streak += 1
        else:
            break
    return streak


def is_streak_freeze_available(session: Session, user_id: uuid.UUID) -> bool:
    """Un congelamiento por mes calendario (UTC) -- se calcula, nunca se
    guarda un contador aparte que pueda desincronizarse de la realidad."""
    today = datetime.now(timezone.utc).date()
    month_start = today.replace(day=1)
    used_this_month = session.exec(
        select(StreakFreeze).where(
            StreakFreeze.user_id == user_id,
            StreakFreeze.date >= month_start,
            StreakFreeze.date <= today,
        )
    ).first()
    return used_this_month is None


def activate_streak_freeze(session: Session, user_id: uuid.UUID) -> int:
    """Protege el dia de HOY para que no rompa la racha. Devuelve la racha
    recalculada. Solo tiene sentido si hay una racha real en curso (si no,
    "congelar" fabricaria una racha de la nada), si no hay actividad real
    hoy todavia, y si no se uso ya el congelamiento del mes -- los tres
    casos levantan un error honesto en vez de silenciosamente no hacer nada."""
    if calculate_streak_days(session, user_id) < 1:
        raise NoActiveStreakError()

    if not is_streak_freeze_available(session, user_id):
        raise StreakFreezeAlreadyUsedError()

    today = datetime.now(timezone.utc).date()
    xp_dates = session.exec(select(XpEvent.created_at).where(XpEvent.user_id == user_id)).all()
    if any(ts.date() == today for ts in xp_dates):
        raise StreakAlreadyActiveError()

    session.add(StreakFreeze(user_id=user_id, date=today))
    session.commit()
    return calculate_streak_days(session, user_id)


def estimate_level(session: Session, user_id: uuid.UUID) -> LevelEstimate | None:
    """
    Aproximacion basada SOLO en evaluaciones (mini test / simulador), no en
    practica libre -- un score tipo examen debe basarse en datos tipo examen.
    None si no hay suficientes evaluaciones completadas todavia.
    """
    attempts = session.exec(
        select(TestAttempt.correct_count, TestAttempt.total_questions).where(
            TestAttempt.user_id == user_id, TestAttempt.completed_at.is_not(None)
        )
    ).all()

    if len(attempts) < MIN_COMPLETED_EVALUATIONS_FOR_LEVEL:
        return None

    total_correct = sum(correct for correct, _ in attempts)
    total_questions = sum(total for _, total in attempts)
    if total_questions == 0:
        return None

    accuracy_ratio = total_correct / total_questions
    score = score_from_accuracy(accuracy_ratio)
    band, band_progress = cefr_band_for_score(score)

    return LevelEstimate(
        estimated_score=score,
        cefr_band=band,
        band_progress_percent=band_progress,
        based_on_attempts=len(attempts),
    )


def calculate_xp_level(user: User) -> XpLevel:
    level = user.current_xp // XP_PER_LEVEL + 1
    current_xp_in_level = user.current_xp % XP_PER_LEVEL
    return XpLevel(level=level, current_xp_in_level=current_xp_in_level, xp_for_next_level=XP_PER_LEVEL)


def calculate_daily_goal(session: Session, user_id: uuid.UUID) -> DailyGoal:
    today = datetime.now(timezone.utc).date()  # ver comentario en calculate_streak_days

    exercise_dates = session.exec(
        select(ExerciseAttempt.created_at).where(ExerciseAttempt.user_id == user_id)
    ).all()
    exercise_today = sum(1 for ts in exercise_dates if ts.date() == today)

    item_dates = session.exec(
        select(TestAttemptItem.answered_at)
        .join(TestAttempt, TestAttempt.id == TestAttemptItem.test_attempt_id)
        .where(TestAttempt.user_id == user_id, TestAttemptItem.answered_at.is_not(None))
    ).all()
    items_today = sum(1 for ts in item_dates if ts.date() == today)

    completed_count = exercise_today + items_today
    return DailyGoal(
        target_count=DAILY_GOAL_TARGET_QUESTIONS,
        completed_count=completed_count,
        completed=completed_count >= DAILY_GOAL_TARGET_QUESTIONS,
    )


def calculate_weekly_evolution(session: Session, user_id: uuid.UUID) -> list[WeeklyEvolutionDay]:
    """Semana calendario actual (Lun-Dom, UTC). Dias sin actividad (incluidos
    los que todavia no llegan) quedan en None -- nunca se fabrica un 0%."""
    today = datetime.now(timezone.utc).date()
    monday = today - timedelta(days=today.weekday())

    exercise_rows = session.exec(
        select(ExerciseAttempt.created_at, ExerciseAttempt.is_correct).where(ExerciseAttempt.user_id == user_id)
    ).all()
    item_rows = session.exec(
        select(TestAttemptItem.answered_at, TestAttemptItem.is_correct)
        .join(TestAttempt, TestAttempt.id == TestAttemptItem.test_attempt_id)
        .where(TestAttempt.user_id == user_id, TestAttemptItem.answered_at.is_not(None))
    ).all()
    all_rows = list(exercise_rows) + list(item_rows)

    days: list[WeeklyEvolutionDay] = []
    for i, label in enumerate(WEEKDAY_LABELS):
        day = monday + timedelta(days=i)
        if day > today:
            days.append(WeeklyEvolutionDay(day_label=label, accuracy_percent=None))
            continue

        day_records = [is_correct for ts, is_correct in all_rows if ts.date() == day]
        if not day_records:
            days.append(WeeklyEvolutionDay(day_label=label, accuracy_percent=None))
            continue

        correct = sum(1 for is_correct in day_records if is_correct)
        days.append(WeeklyEvolutionDay(day_label=label, accuracy_percent=round(correct / len(day_records) * 100, 1)))

    return days


def calculate_study_statistics(session: Session, user: User) -> StudyStatistics:
    records = _collect_answer_records(session, user.id)
    questions_answered = len(records)
    correct = sum(1 for _, is_correct in records if is_correct)
    incorrect = questions_answered - correct
    accuracy_percent = round(correct / questions_answered * 100, 1) if questions_answered else None

    unanswered_count = session.exec(
        select(func.count())
        .select_from(TestAttemptItem)
        .join(TestAttempt, TestAttempt.id == TestAttemptItem.test_attempt_id)
        .where(
            TestAttempt.user_id == user.id,
            TestAttempt.completed_at.is_not(None),
            TestAttemptItem.selected_answer.is_(None),
        )
    ).one()

    exercise_time = session.exec(
        select(func.coalesce(func.sum(ExerciseAttempt.time_spent_seconds), 0)).where(
            ExerciseAttempt.user_id == user.id
        )
    ).one()

    completed_evaluations = session.exec(
        select(TestAttempt.started_at, TestAttempt.completed_at, TestAttempt.test_type).where(
            TestAttempt.user_id == user.id, TestAttempt.completed_at.is_not(None)
        )
    ).all()
    evaluation_time = sum(
        (completed_at - started_at).total_seconds() for started_at, completed_at, _ in completed_evaluations
    )

    completed_simulators = sum(1 for _, _, t in completed_evaluations if t == TestType.simulator)
    completed_mini_tests = sum(1 for _, _, t in completed_evaluations if t == TestType.mini_test)

    return StudyStatistics(
        questions_answered=questions_answered,
        accuracy_percent=accuracy_percent,
        study_time_seconds=int(exercise_time) + int(evaluation_time),
        completed_simulators=completed_simulators,
        completed_mini_tests=completed_mini_tests,
        day_streak=calculate_streak_days(session, user.id),
        correct_count=correct,
        incorrect_count=incorrect,
        unanswered_count=unanswered_count,
    )


def get_dashboard_summary(session: Session, user: User) -> DashboardSummary:
    streak = calculate_streak_days(session, user.id)
    records = _collect_answer_records(session, user.id)

    has_enough_data = len(records) >= MIN_TOTAL_ATTEMPTS_FOR_RECOMMENDATIONS
    weak_skills = calculate_weak_skills(session, user.id) if has_enough_data else []
    quick_practice = calculate_quick_practice(session, user.id) if has_enough_data else []

    level = estimate_level(session, user.id)

    return DashboardSummary(
        current_xp=user.current_xp,
        streak_days=streak,
        weak_skills=weak_skills,
        quick_practice=quick_practice,
        has_enough_data_for_recommendations=has_enough_data,
        xp_level=calculate_xp_level(user),
        level=level,
        has_enough_data_for_level=level is not None,
        daily_goal=calculate_daily_goal(session, user.id),
        streak_freeze_available=is_streak_freeze_available(session, user.id),
    )
