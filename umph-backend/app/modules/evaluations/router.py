import uuid

from fastapi import APIRouter

from app.modules.evaluations.models import TestType
from app.modules.evaluations.schemas import (
    InProgressAttempt,
    PassageContext,
    SectionScore,
    StartMiniTestRequest,
    SubmitTestAnswerRequest,
    SubmitTestAnswerResponse,
    TestAttemptItemPublic,
    TestAttemptStarted,
    TestAttemptSummary,
    TestResult,
)
from app.modules.evaluations.service import (
    SIMULATOR_TIME_LIMIT_SECONDS,
    build_test_result,
    complete_attempt,
    count_answered_items,
    get_attempt,
    get_attempt_items_with_questions,
    get_completed_result,
    get_in_progress_attempt,
    get_passages_for_attempt,
    list_completed_attempts,
    start_mini_test,
    start_simulator,
    submit_answer,
)
from app.modules.learning.schemas import QuestionPublic
from app.shared.dependencies import CurrentUserDep, SessionDep

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


def _build_started_response(session: SessionDep, attempt) -> TestAttemptStarted:
    items_with_questions = get_attempt_items_with_questions(session, attempt.id)
    questions = [q for _, q in items_with_questions]
    passages = get_passages_for_attempt(session, questions)

    return TestAttemptStarted(
        test_attempt_id=attempt.id,
        test_type=attempt.test_type,
        mini_test_mode=attempt.mini_test_mode,
        total_questions=attempt.total_questions,
        time_limit_seconds=SIMULATOR_TIME_LIMIT_SECONDS if attempt.test_type == TestType.simulator else None,
        started_at=attempt.started_at,
        items=[
            TestAttemptItemPublic(
                order_index=item.order_index,
                question=QuestionPublic.model_validate(question),
                answered=item.selected_answer is not None,
                selected_answer=item.selected_answer,
            )
            for item, question in items_with_questions
        ],
        passages=[PassageContext(id=p.id, title=p.title, text=p.text) for p in passages],
    )


@router.post("/mini-tests", response_model=TestAttemptStarted)
def create_mini_test(data: StartMiniTestRequest, session: SessionDep, current_user: CurrentUserDep) -> TestAttemptStarted:
    attempt = start_mini_test(session, current_user, data.mode, data.num_questions)
    return _build_started_response(session, attempt)


@router.post("/simulator", response_model=TestAttemptStarted)
def create_simulator(session: SessionDep, current_user: CurrentUserDep) -> TestAttemptStarted:
    attempt = start_simulator(session, current_user)
    return _build_started_response(session, attempt)


@router.get("/attempts/in-progress", response_model=InProgressAttempt | None)
def read_in_progress_attempt(session: SessionDep, current_user: CurrentUserDep) -> InProgressAttempt | None:
    # Registrada antes de /attempts/{attempt_id} a proposito: "in-progress"
    # no debe intentar parsearse como UUID.
    attempt = get_in_progress_attempt(session, current_user)
    if attempt is None:
        return None
    return InProgressAttempt(
        id=attempt.id,
        test_type=attempt.test_type,
        mini_test_mode=attempt.mini_test_mode,
        total_questions=attempt.total_questions,
        answered_count=count_answered_items(session, attempt.id),
        started_at=attempt.started_at,
    )


@router.get("/attempts/{attempt_id}", response_model=TestAttemptStarted)
def read_attempt(attempt_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep) -> TestAttemptStarted:
    attempt = get_attempt(session, current_user, attempt_id)
    return _build_started_response(session, attempt)


@router.post("/attempts/{attempt_id}/answers", response_model=SubmitTestAnswerResponse)
def answer_attempt_question(
    attempt_id: uuid.UUID, data: SubmitTestAnswerRequest, session: SessionDep, current_user: CurrentUserDep
) -> SubmitTestAnswerResponse:
    attempt = get_attempt(session, current_user, attempt_id)
    is_correct, question = submit_answer(session, current_user, attempt_id, data.question_id, data.selected_answer)

    # Durante el Simulador: nunca se revela si fue correcta ni la
    # explicacion -- "No IA, no ayudas, no explicaciones" hasta el final.
    if attempt.test_type == TestType.simulator:
        return SubmitTestAnswerResponse(recorded=True, is_correct=None, correct_answer=None, explanation=None)

    return SubmitTestAnswerResponse(
        recorded=True,
        is_correct=is_correct,
        correct_answer=question.correct_answer,
        explanation=question.explanation,
    )


@router.post("/attempts/{attempt_id}/complete", response_model=TestResult)
def finish_attempt(attempt_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep) -> TestResult:
    attempt, xp_awarded = complete_attempt(session, current_user, attempt_id)
    return build_test_result(attempt, xp_awarded)


@router.get("/history", response_model=list[TestAttemptSummary])
def read_history(session: SessionDep, current_user: CurrentUserDep) -> list[TestAttemptSummary]:
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


@router.get("/attempts/{attempt_id}/result", response_model=TestResult)
def read_result(attempt_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep) -> TestResult:
    attempt = get_completed_result(session, current_user, attempt_id)
    # xp_awarded no se vuelve a calcular (ya se otorgo al completar);
    # se muestra 0 aqui porque esta vista es solo de consulta historica.
    return build_test_result(attempt, xp_awarded=0)
