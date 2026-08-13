from fastapi import APIRouter

from app.modules.ai.schemas import (
    ExplainQuestionRequest,
    ExplainQuestionResponse,
    RecommendationResponse,
    RecommendPracticeRequest,
)
from app.modules.ai.service import explain_question, recommend_practice
from app.shared.dependencies import CurrentUserDep, SessionDep

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/explain", response_model=ExplainQuestionResponse)
def explain(
    data: ExplainQuestionRequest, session: SessionDep, current_user: CurrentUserDep
) -> ExplainQuestionResponse:
    payload, source = explain_question(session, data.question_id, data.student_answer)
    return ExplainQuestionResponse(**payload.model_dump(), source=source)


@router.post("/recommend-practice", response_model=RecommendationResponse)
def recommend(
    data: RecommendPracticeRequest, session: SessionDep, current_user: CurrentUserDep
) -> RecommendationResponse:
    recommendation, source = recommend_practice(session, current_user, data.attempt_id)
    return RecommendationResponse(recommendation=recommendation, source=source)
