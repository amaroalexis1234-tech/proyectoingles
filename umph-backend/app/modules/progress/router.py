import uuid

from fastapi import APIRouter

from app.modules.evaluations.schemas import TestAttemptSummary, TestResult
from app.modules.evaluations.service import build_test_result, get_completed_result, list_completed_attempts
from app.modules.progress.schemas import DashboardSummary, StudyStatistics, WeeklyEvolutionDay
from app.modules.progress.service import (
    activate_streak_freeze,
    calculate_study_statistics,
    calculate_weekly_evolution,
    get_dashboard_summary,
)
from app.shared.dependencies import CurrentUserDep, SessionDep

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/dashboard", response_model=DashboardSummary)
def read_dashboard_summary(current_user: CurrentUserDep, session: SessionDep) -> DashboardSummary:
    return get_dashboard_summary(session, current_user)


@router.post("/streak-freeze", response_model=DashboardSummary)
def activate_streak_freeze_endpoint(current_user: CurrentUserDep, session: SessionDep) -> DashboardSummary:
    activate_streak_freeze(session, current_user.id)
    return get_dashboard_summary(session, current_user)


@router.get("/stats", response_model=StudyStatistics)
def read_study_statistics(current_user: CurrentUserDep, session: SessionDep) -> StudyStatistics:
    return calculate_study_statistics(session, current_user)


@router.get("/weekly-evolution", response_model=list[WeeklyEvolutionDay])
def read_weekly_evolution(current_user: CurrentUserDep, session: SessionDep) -> list[WeeklyEvolutionDay]:
    return calculate_weekly_evolution(session, current_user.id)


@router.get("/history", response_model=list[TestAttemptSummary])
def read_progress_history(session: SessionDep, current_user: CurrentUserDep) -> list[TestAttemptSummary]:
    attempts = list_completed_attempts(session, current_user)
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


@router.get("/results/{attempt_id}", response_model=TestResult)
def read_progress_result(attempt_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep) -> TestResult:
    attempt = get_completed_result(session, current_user, attempt_id)
    return build_test_result(attempt, xp_awarded=0)
