import uuid

from fastapi import APIRouter
from sqlmodel import Session, select

from app.modules.auth.models import User
from app.modules.evaluations.models import TestAttemptItem
from app.modules.evaluations.schemas import TestAttemptSummary
from app.modules.evaluations.service import list_completed_attempts
from app.modules.learning.models import ExerciseAttempt
from app.modules.progress.schemas import DashboardSummary, StudyStatistics
from app.modules.progress.service import calculate_streak_days, calculate_study_statistics, get_dashboard_summary
from app.modules.question_bank.models import Question
from app.modules.teacher.schemas import QuestionAnalytics, QuestionAnalyticsResponse, StudentSummary
from app.shared.dependencies import CurrentTeacherDep, SessionDep
from app.shared.exceptions import UserNotFoundError

router = APIRouter(prefix="/teacher", tags=["teacher"])


def _get_student(session: Session, student_id: uuid.UUID) -> User:
    """
    Valida que el id exista Y sea un alumno -- un maestro no puede usar esta
    via para ver los datos de otro maestro.
    """
    student = session.get(User, student_id)
    if student is None or student.role != "student":
        raise UserNotFoundError()
    return student


@router.get("/students", response_model=list[StudentSummary])
def list_students(session: SessionDep, current_teacher: CurrentTeacherDep) -> list[StudentSummary]:
    students = session.exec(select(User).where(User.role == "student")).all()
    return [
        StudentSummary(
            id=s.id,
            full_name=s.full_name,
            email=s.email,
            current_xp=s.current_xp,
            streak_days=calculate_streak_days(session, s.id),
        )
        for s in students
    ]


@router.get("/students/{student_id}/summary", response_model=DashboardSummary)
def read_student_summary(
    student_id: uuid.UUID, session: SessionDep, current_teacher: CurrentTeacherDep
) -> DashboardSummary:
    student = _get_student(session, student_id)
    # Misma funcion que ya usa el alumno para su propio dashboard -- cero
    # logica nueva, solo se le pasa el alumno objetivo en vez de current_user.
    return get_dashboard_summary(session, student)


@router.get("/students/{student_id}/stats", response_model=StudyStatistics)
def read_student_stats(
    student_id: uuid.UUID, session: SessionDep, current_teacher: CurrentTeacherDep
) -> StudyStatistics:
    student = _get_student(session, student_id)
    return calculate_study_statistics(session, student)


@router.get("/students/{student_id}/history", response_model=list[TestAttemptSummary])
def read_student_history(
    student_id: uuid.UUID, session: SessionDep, current_teacher: CurrentTeacherDep
) -> list[TestAttemptSummary]:
    student = _get_student(session, student_id)
    attempts = list_completed_attempts(session, student)
    return [
        TestAttemptSummary(
            id=a.id,
            test_type=a.test_type,
            mini_test_mode=a.mini_test_mode,
            completed_at=a.completed_at,
            total_questions=a.total_questions,
            correct_count=a.correct_count,
            accuracy=round((a.correct_count / a.total_questions) * 100, 1) if a.total_questions else 0.0,
        )
        for a in attempts
    ]


@router.get("/questions/analytics", response_model=QuestionAnalyticsResponse)
def read_question_analytics(session: SessionDep, current_teacher: CurrentTeacherDep) -> QuestionAnalyticsResponse:
    """
    Precision real por pregunta, combinando Mini Test/Simulador
    (test_attempt_items, solo filas ya respondidas) y practica libre
    (exercise_attempts) -- ambas son intentos reales del alumno sobre esa
    pregunta. Ordenado de peor a mejor precision: son las que mas vale la
    pena que el maestro revise primero.
    """
    questions = session.exec(select(Question)).all()

    stats: dict[uuid.UUID, list[int]] = {}

    test_rows = session.exec(
        select(TestAttemptItem.question_id, TestAttemptItem.is_correct).where(
            TestAttemptItem.selected_answer.is_not(None)
        )
    ).all()
    for question_id, is_correct in test_rows:
        bucket = stats.setdefault(question_id, [0, 0])
        bucket[0] += 1
        if is_correct:
            bucket[1] += 1

    exercise_rows = session.exec(select(ExerciseAttempt.question_id, ExerciseAttempt.is_correct)).all()
    for question_id, is_correct in exercise_rows:
        bucket = stats.setdefault(question_id, [0, 0])
        bucket[0] += 1
        if is_correct:
            bucket[1] += 1

    questions_by_id = {q.id: q for q in questions}

    results: list[QuestionAnalytics] = []
    for question_id, (attempts, correct) in stats.items():
        question = questions_by_id.get(question_id)
        if question is None:
            continue  # pregunta borrada despues de ser respondida -- se ignora, no se fabrica
        results.append(
            QuestionAnalytics(
                question_id=question.id,
                section=question.section.value,
                prompt=question.prompt,
                attempts_count=attempts,
                correct_count=correct,
                accuracy_percent=round(correct / attempts * 100, 1),
            )
        )

    results.sort(key=lambda r: r.accuracy_percent)
    untried_count = len(questions) - len(results)

    return QuestionAnalyticsResponse(questions=results, untried_count=untried_count)
