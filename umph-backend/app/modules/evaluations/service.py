import random
import uuid
from datetime import datetime, timezone

from sqlalchemy import func
from sqlmodel import Session, select

from app.modules.auth.models import User
from app.modules.evaluations.models import MiniTestMode, TestAttempt, TestAttemptItem, TestType
from app.modules.evaluations.schemas import SectionScore, TestResult
from app.modules.evaluations.schemas import SectionScore
from app.modules.progress.models import XpReason
from app.modules.progress.service import record_xp_event
from app.modules.question_bank.models import Passage, Question, Section
from app.shared.exceptions import DomainError

# XP por evaluacion completada (mayor que una pregunta suelta de Learning,
# porque representa un esfuerzo sostenido).
XP_MINI_TEST_COMPLETED = 30
XP_SIMULATOR_COMPLETED = 100

SIMULATOR_STRUCTURE_COUNT = 15
SIMULATOR_WRITTEN_EXPRESSION_COUNT = 25
SIMULATOR_READING_PASSAGE_COUNT = 5
SIMULATOR_TIME_LIMIT_SECONDS = 25 * 60 + 55 * 60  # 25 min Section 2 + 55 min Section 3 = 80 min total

OFFICIAL_MINI_TEST_STRUCTURE_COUNT = 10
OFFICIAL_MINI_TEST_WRITTEN_EXPRESSION_COUNT = 10
OFFICIAL_MINI_TEST_VOCABULARY_COUNT = 10


class TestAttemptNotFoundError(DomainError):
    def __init__(self) -> None:
        super().__init__("La evaluación no existe.")


class TestAttemptNotOwnedError(DomainError):
    def __init__(self) -> None:
        super().__init__("Esta evaluación no pertenece al usuario actual.")


class TestAttemptAlreadyCompletedError(DomainError):
    def __init__(self) -> None:
        super().__init__("Esta evaluación ya fue completada.")


class QuestionNotInAttemptError(DomainError):
    def __init__(self) -> None:
        super().__init__("Esa pregunta no forma parte de esta evaluación.")


def _pick_random(session: Session, section: Section, count: int) -> list[Question]:
    questions = session.exec(select(Question).where(Question.section == section)).all()
    random.shuffle(questions)
    return questions[:count]


def _pick_reading_passages(session: Session, passage_count: int) -> list[Passage]:
    passages = session.exec(select(Passage)).all()
    random.shuffle(passages)
    return passages[:passage_count]


def _create_attempt_with_questions(
    session: Session,
    user: User,
    test_type: TestType,
    mini_test_mode: MiniTestMode | None,
    questions: list[Question],
) -> TestAttempt:
    attempt = TestAttempt(
        user_id=user.id,
        test_type=test_type,
        mini_test_mode=mini_test_mode,
        started_at=datetime.now(timezone.utc),
        total_questions=len(questions),
    )
    session.add(attempt)
    session.commit()
    session.refresh(attempt)

    for index, question in enumerate(questions):
        session.add(TestAttemptItem(test_attempt_id=attempt.id, question_id=question.id, order_index=index))
    session.commit()

    return attempt


def start_mini_test(session: Session, user: User, mode: MiniTestMode, num_questions: int) -> TestAttempt:
    if mode == MiniTestMode.grammar:
        half = num_questions // 2
        questions = _pick_random(session, Section.structure, half) + _pick_random(
            session, Section.written_expression, num_questions - half
        )
    elif mode == MiniTestMode.mixed:
        half = num_questions // 2
        questions = _pick_random(session, Section.structure, half // 2)
        questions += _pick_random(session, Section.written_expression, half - half // 2)
        questions += _pick_random(session, Section.vocabulary, num_questions - len(questions))
    elif mode == MiniTestMode.reading:
        passages = _pick_reading_passages(session, 1)
        questions = list(
            session.exec(select(Question).where(Question.passage_id == passages[0].id))
        )
    elif mode == MiniTestMode.official:
        questions = (
            _pick_random(session, Section.structure, OFFICIAL_MINI_TEST_STRUCTURE_COUNT)
            + _pick_random(session, Section.written_expression, OFFICIAL_MINI_TEST_WRITTEN_EXPRESSION_COUNT)
            + _pick_random(session, Section.vocabulary, OFFICIAL_MINI_TEST_VOCABULARY_COUNT)
        )
        passages = _pick_reading_passages(session, 1)
        questions += list(session.exec(select(Question).where(Question.passage_id == passages[0].id)))
    else:
        questions = []

    random.shuffle(questions)
    return _create_attempt_with_questions(session, user, TestType.mini_test, mode, questions)


def start_simulator(session: Session, user: User) -> TestAttempt:
    questions = _pick_random(session, Section.structure, SIMULATOR_STRUCTURE_COUNT)
    questions += _pick_random(session, Section.written_expression, SIMULATOR_WRITTEN_EXPRESSION_COUNT)

    passages = _pick_reading_passages(session, SIMULATOR_READING_PASSAGE_COUNT)
    for passage in passages:
        questions += list(session.exec(select(Question).where(Question.passage_id == passage.id)))

    # No se mezcla el orden entre Section 2 y Section 3: el simulador
    # respeta el orden real del examen (Structure+WE primero, Reading despues).
    attempt = _create_attempt_with_questions(session, user, TestType.simulator, None, questions)
    return attempt


def get_in_progress_attempt(session: Session, user: User) -> TestAttempt | None:
    return session.exec(
        select(TestAttempt)
        .where(TestAttempt.user_id == user.id, TestAttempt.completed_at.is_(None))
        .order_by(TestAttempt.started_at.desc())
    ).first()


def count_answered_items(session: Session, attempt_id: uuid.UUID) -> int:
    return session.exec(
        select(func.count())
        .select_from(TestAttemptItem)
        .where(TestAttemptItem.test_attempt_id == attempt_id, TestAttemptItem.selected_answer.is_not(None))
    ).one()


def get_attempt(session: Session, user: User, attempt_id: uuid.UUID) -> TestAttempt:
    attempt = session.get(TestAttempt, attempt_id)
    if attempt is None:
        raise TestAttemptNotFoundError()
    if attempt.user_id != user.id:
        raise TestAttemptNotOwnedError()
    return attempt


def get_attempt_items_with_questions(session: Session, attempt_id: uuid.UUID) -> list[tuple[TestAttemptItem, Question]]:
    items = session.exec(
        select(TestAttemptItem)
        .where(TestAttemptItem.test_attempt_id == attempt_id)
        .order_by(TestAttemptItem.order_index)
    ).all()
    result = []
    for item in items:
        question = session.get(Question, item.question_id)
        result.append((item, question))
    return result


def get_passages_for_attempt(session: Session, questions: list[Question]) -> list[Passage]:
    passage_ids = {q.passage_id for q in questions if q.passage_id is not None}
    return [session.get(Passage, pid) for pid in passage_ids]


def submit_answer(
    session: Session, user: User, attempt_id: uuid.UUID, question_id: uuid.UUID, selected_answer: str
) -> tuple[bool, Question]:
    attempt = get_attempt(session, user, attempt_id)
    if attempt.completed_at is not None:
        raise TestAttemptAlreadyCompletedError()

    item = session.exec(
        select(TestAttemptItem).where(
            TestAttemptItem.test_attempt_id == attempt_id, TestAttemptItem.question_id == question_id
        )
    ).first()
    if item is None:
        raise QuestionNotInAttemptError()

    question = session.get(Question, question_id)
    is_correct = selected_answer.upper() == question.correct_answer.upper()

    item.selected_answer = selected_answer.upper()
    item.is_correct = is_correct
    item.answered_at = datetime.now(timezone.utc)
    session.add(item)
    session.commit()

    return is_correct, question


def build_test_result(attempt: TestAttempt, xp_awarded: int) -> TestResult:
    accuracy = round((attempt.correct_count / attempt.total_questions) * 100, 1) if attempt.total_questions else 0.0
    # completed_at siempre esta seteado aqui: los dos call sites (complete_attempt
    # y get_completed_result) garantizan que el intento ya esta completado.
    assert attempt.completed_at is not None
    return TestResult(
        test_attempt_id=attempt.id,
        total_questions=attempt.total_questions,
        correct_count=attempt.correct_count,
        accuracy=accuracy,
        section_scores={k: SectionScore(**v) for k, v in attempt.section_scores.items()},
        xp_awarded=xp_awarded,
        started_at=attempt.started_at,
        completed_at=attempt.completed_at,
    )


def list_completed_attempts(session: Session, user: User) -> list[TestAttempt]:
    return session.exec(
        select(TestAttempt)
        .where(TestAttempt.user_id == user.id, TestAttempt.completed_at.is_not(None))
        .order_by(TestAttempt.completed_at.desc())
    ).all()


def get_completed_result(session: Session, user: User, attempt_id: uuid.UUID) -> TestAttempt:
    attempt = get_attempt(session, user, attempt_id)
    if attempt.completed_at is None:
        raise TestAttemptNotFoundError()
    return attempt


def complete_attempt(session: Session, user: User, attempt_id: uuid.UUID) -> tuple[TestAttempt, int]:
    attempt = get_attempt(session, user, attempt_id)
    if attempt.completed_at is not None:
        raise TestAttemptAlreadyCompletedError()

    items_with_questions = get_attempt_items_with_questions(session, attempt_id)

    section_scores: dict[str, SectionScore] = {}
    correct_count = 0
    for item, question in items_with_questions:
        section_key = question.section.value
        current = section_scores.get(section_key, SectionScore(correct=0, total=0))
        current.total += 1
        if item.is_correct:
            current.correct += 1
            correct_count += 1
        section_scores[section_key] = current

    attempt.completed_at = datetime.now(timezone.utc)
    attempt.correct_count = correct_count
    attempt.section_scores = {k: v.model_dump() for k, v in section_scores.items()}
    session.add(attempt)
    session.commit()
    session.refresh(attempt)

    xp_reason = (
        XpReason.simulator_completed if attempt.test_type == TestType.simulator else XpReason.mini_test_completed
    )
    xp_amount = XP_SIMULATOR_COMPLETED if attempt.test_type == TestType.simulator else XP_MINI_TEST_COMPLETED
    record_xp_event(session, user, xp_amount, xp_reason)

    return attempt, xp_amount
