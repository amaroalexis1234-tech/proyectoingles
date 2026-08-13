import random
import uuid

from sqlmodel import Session, select

from app.modules.auth.models import User
from app.modules.learning.models import ExerciseAttempt
from app.modules.progress.models import XpReason
from app.modules.progress.service import record_xp_event
from app.modules.question_bank.models import Passage, Question, Section
from app.shared.exceptions import DomainError

XP_PER_CORRECT_ANSWER = 10

# Reading no se sirve por esta funcion: sus preguntas siempre van
# acompañadas del passage (ver get_passage_with_questions).
NON_READING_SECTIONS = [Section.structure, Section.written_expression, Section.vocabulary]


class QuestionNotFoundError(DomainError):
    def __init__(self) -> None:
        super().__init__("La pregunta no existe.")


class InvalidSectionForExercisesError(DomainError):
    def __init__(self) -> None:
        super().__init__("Reading se sirve por passage, no como lista suelta de preguntas.")


def get_exercises(session: Session, section: Section, limit: int) -> list[Question]:
    if section not in NON_READING_SECTIONS:
        raise InvalidSectionForExercisesError()

    questions = session.exec(select(Question).where(Question.section == section)).all()
    random.shuffle(questions)
    return questions[:limit]


def list_reading_passages(session: Session) -> list[Passage]:
    return session.exec(select(Passage)).all()


def get_passage_with_questions(session: Session, passage_id: uuid.UUID) -> tuple[Passage, list[Question]]:
    passage = session.get(Passage, passage_id)
    if passage is None:
        raise QuestionNotFoundError()
    questions = session.exec(select(Question).where(Question.passage_id == passage_id)).all()
    return passage, questions


def submit_attempt(
    session: Session,
    user: User,
    question_id: uuid.UUID,
    selected_answer: str,
    time_spent_seconds: int | None,
) -> tuple[ExerciseAttempt, Question, int]:
    question = session.get(Question, question_id)
    if question is None:
        raise QuestionNotFoundError()

    is_correct = selected_answer.upper() == question.correct_answer.upper()

    attempt = ExerciseAttempt(
        user_id=user.id,
        question_id=question.id,
        selected_answer=selected_answer.upper(),
        is_correct=is_correct,
        time_spent_seconds=time_spent_seconds,
    )
    session.add(attempt)
    session.commit()
    session.refresh(attempt)

    xp_awarded = 0
    if is_correct:
        record_xp_event(session, user, XP_PER_CORRECT_ANSWER, XpReason.correct_answer)
        xp_awarded = XP_PER_CORRECT_ANSWER

    return attempt, question, xp_awarded
