import uuid

from fastapi import APIRouter, Query

from app.modules.learning.schemas import (
    PassageSummary,
    PassageWithQuestions,
    QuestionPublic,
    SubmitAttemptRequest,
    SubmitAttemptResponse,
)
from app.modules.learning.service import (
    get_exercises,
    get_passage_with_questions,
    list_reading_passages,
    submit_attempt,
)
from app.modules.question_bank.models import Section
from app.shared.dependencies import CurrentUserDep, SessionDep

router = APIRouter(prefix="/learning", tags=["learning"])


@router.get("/exercises", response_model=list[QuestionPublic])
def read_exercises(
    session: SessionDep,
    current_user: CurrentUserDep,
    section: Section = Query(..., description="structure | written_expression | vocabulary"),
    limit: int = Query(default=10, ge=1, le=50),
) -> list[QuestionPublic]:
    questions = get_exercises(session, section, limit)
    return [QuestionPublic.model_validate(q) for q in questions]


@router.get("/reading/passages", response_model=list[PassageSummary])
def read_reading_passages(session: SessionDep, current_user: CurrentUserDep) -> list[PassageSummary]:
    passages = list_reading_passages(session)
    return [PassageSummary.model_validate(p) for p in passages]


@router.get("/reading/passages/{passage_id}", response_model=PassageWithQuestions)
def read_passage_with_questions(
    passage_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep
) -> PassageWithQuestions:
    passage, questions = get_passage_with_questions(session, passage_id)
    return PassageWithQuestions(
        passage_id=passage.id,
        title=passage.title,
        text=passage.text,
        questions=[QuestionPublic.model_validate(q) for q in questions],
    )


@router.post("/attempts", response_model=SubmitAttemptResponse)
def create_attempt(
    data: SubmitAttemptRequest, session: SessionDep, current_user: CurrentUserDep
) -> SubmitAttemptResponse:
    attempt, question, xp_awarded = submit_attempt(
        session, current_user, data.question_id, data.selected_answer, data.time_spent_seconds
    )
    return SubmitAttemptResponse(
        is_correct=attempt.is_correct,
        correct_answer=question.correct_answer,
        explanation=question.explanation,
        xp_awarded=xp_awarded,
    )
