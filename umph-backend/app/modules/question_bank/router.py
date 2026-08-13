import uuid

from fastapi import APIRouter, File, Query, UploadFile, status

from app.modules.question_bank.models import Section
from app.modules.question_bank.schemas import (
    PassageCreate,
    PassageRead,
    QuestionCreate,
    QuestionImportError,
    QuestionImportResult,
    QuestionRead,
    QuestionUpdate,
)
from app.modules.question_bank.service import (
    create_passage,
    create_question,
    delete_question,
    import_questions_from_csv,
    list_passages,
    list_questions,
    update_question,
)
from app.shared.dependencies import CurrentTeacherDep, SessionDep

router = APIRouter(prefix="/question-bank", tags=["question-bank"])


@router.post("/questions", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
def create_question_endpoint(
    data: QuestionCreate, session: SessionDep, current_teacher: CurrentTeacherDep
) -> QuestionRead:
    question = create_question(session, current_teacher, data)
    return QuestionRead.model_validate(question)


@router.post("/questions/import", response_model=QuestionImportResult)
async def import_questions_endpoint(
    session: SessionDep, current_teacher: CurrentTeacherDep, file: UploadFile = File(...)
) -> QuestionImportResult:
    file_bytes = await file.read()
    created, errors = import_questions_from_csv(session, current_teacher, file_bytes)
    return QuestionImportResult(created=created, errors=[QuestionImportError(**e) for e in errors])


@router.get("/questions", response_model=list[QuestionRead])
def list_questions_endpoint(
    session: SessionDep,
    current_teacher: CurrentTeacherDep,
    section: Section | None = Query(default=None),
) -> list[QuestionRead]:
    questions = list_questions(session, section)
    return [QuestionRead.model_validate(q) for q in questions]


@router.patch("/questions/{question_id}", response_model=QuestionRead)
def update_question_endpoint(
    question_id: uuid.UUID, data: QuestionUpdate, session: SessionDep, current_teacher: CurrentTeacherDep
) -> QuestionRead:
    question = update_question(session, question_id, data)
    return QuestionRead.model_validate(question)


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question_endpoint(
    question_id: uuid.UUID, session: SessionDep, current_teacher: CurrentTeacherDep
) -> None:
    delete_question(session, question_id)


@router.post("/passages", response_model=PassageRead, status_code=status.HTTP_201_CREATED)
def create_passage_endpoint(
    data: PassageCreate, session: SessionDep, current_teacher: CurrentTeacherDep
) -> PassageRead:
    passage = create_passage(session, current_teacher, data)
    return PassageRead.model_validate(passage)


@router.get("/passages", response_model=list[PassageRead])
def list_passages_endpoint(session: SessionDep, current_teacher: CurrentTeacherDep) -> list[PassageRead]:
    passages = list_passages(session)
    return [PassageRead.model_validate(p) for p in passages]
