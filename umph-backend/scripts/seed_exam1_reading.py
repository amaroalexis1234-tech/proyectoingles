"""
Carga las preguntas de Reading Comprehension del "Exam 1" extraidas de
TOEFL_tests_2026.pdf (paginas 343-349): 5 passages, 50 preguntas.

Mismo criterio que scripts/seed_exam1_structure.py: las respuestas fueron
determinadas por comprension de lectura (no copiadas de un answer key
oficial, esa pagina no fue extraida), por eso verified=False en todas.

IMPORTANTE: los numeros de skill de Reading (1-13) son un catalogo
DISTINTO al de Structure/Written Expression (1-60) -- por eso el modelo
Skill distingue por (section, number).

Uso:
    python -m scripts.seed_exam1_reading
"""
from sqlmodel import Session, select

from app.core.database import engine
from app.modules.question_bank.models import Passage, Question, QuestionType, Section, Skill

SOURCE = "TOEFL_tests_2026.pdf - Exam 1 Reading Comprehension (p.343-349)"

PASSAGES = [
    {
        "key": "carbon_tetrachloride",
        "title": "Carbon Tetrachloride",
        "text": (
            "Carbon tetrachloride is a colorless and inflammable liquid that can be produced by "
            "combining carbon disulfide and chlorine. This compound is widely used in industry "
            "today because of its effectiveness as a solvent as well as its use in the production "
            "of propellants.\n\n"
            "Despite its widespread use in industry, carbon tetrachloride has been banned for home "
            "use. In the past, carbon tetrachloride was a common ingredient in cleaning compounds "
            "that were used throughout the home, but it was found to be dangerous: when heated, it "
            "changes into a poisonous gas that can cause severe illness and even death if it is "
            "inhaled. Because of this dangerous characteristic, the United States revoked "
            "permission for the home use of carbon tetrachloride in 1970. The United States has "
            "taken similar action with various other chemical compounds."
        ),
        "questions": [
            {
                "prompt": "The main point of this passage is that",
                "options": {
                    "A": "carbon tetrachloride can be very dangerous when it is heated",
                    "B": "the government banned carbon tetrachloride in 1970",
                    "C": "although carbon tetrachloride can legally be used in industry, it is not allowed in home products",
                    "D": "carbon tetrachloride used to be a regular part of cleaning compounds",
                },
                "correct_answer": "C",
                "skill": 1,
            },
            {
                "prompt": 'The word "widely" in line 2 could most easily be replaced by',
                "options": {"A": "grandly", "B": "extensively", "C": "largely", "D": "hugely"},
                "correct_answer": "B",
                "skill": 11,
            },
            {
                "prompt": 'The word "banned" in line 4 is closest in meaning to',
                "options": {"A": "forbidden", "B": "allowed", "C": "suggested", "D": "instituted"},
                "correct_answer": "A",
                "skill": 10,
            },
            {
                "prompt": "According to the passage, before 1970 carbon tetrachloride was",
                "options": {
                    "A": "used by itself as a cleanser",
                    "B": "banned in industrial use",
                    "C": "often used as a component of cleaning products",
                    "D": "not allowed in home cleaning products",
                },
                "correct_answer": "C",
                "skill": 3,
            },
            {
                "prompt": "It is stated in the passage that when carbon tetrachloride is heated, it becomes",
                "options": {"A": "harmful", "B": "colorless", "C": "a cleaning compound", "D": "inflammable"},
                "correct_answer": "A",
                "skill": 3,
            },
            {
                "prompt": 'The word "inhaled" in line 7 is closest in meaning to',
                "options": {"A": "warmed", "B": "breathed in", "C": "carelessly used", "D": "blown"},
                "correct_answer": "B",
                "skill": 9,
            },
            {
                "prompt": 'The word "revoked" in line 8 could most easily be replaced by',
                "options": {"A": "gave", "B": "granted", "C": "instituted", "D": "took away"},
                "correct_answer": "D",
                "skill": 10,
            },
            {
                "prompt": "It can be inferred from the passage that one role of the U.S. government is to",
                "options": {
                    "A": "regulate product safety",
                    "B": "prohibit any use of carbon tetrachloride",
                    "C": "instruct industry on cleaning methodologies",
                    "D": "ban the use of any chemicals",
                },
                "correct_answer": "A",
                "skill": 6,
            },
            {
                "prompt": "The paragraph following the passage most likely discusses",
                "options": {
                    "A": "additional uses for carbon tetrachloride",
                    "B": "the banning of various chemical compounds by the U.S. government",
                    "C": "further dangerous effects of carbon tetrachloride",
                    "D": "the major characteristics of carbon tetrachloride",
                },
                "correct_answer": "B",
                "skill": 7,
            },
        ],
    },
    {
        "key": "whistler",
        "title": "James Whistler",
        "text": (
            "The next artist in this survey of American artists is James Whistler; he is included "
            "in this survey of American artists because he was born in the United States, although "
            "the majority of his artwork was completed in Europe. Whistler was born in "
            "Massachusetts in 1834, but nine years later his father moved the family to St. "
            "Petersburg, Russia, to work on the construction of a railroad. The family returned to "
            "the United States in 1849. Two years later Whistler entered the U.S. military academy "
            "at West Point, but he was unable to graduate. At the age of twenty-one, Whistler went "
            "to Europe to study art despite familial objections, and he remained in Europe until "
            "his death.\n\n"
            "Whistler worked in various art forms, including etchings and lithographs. However, he "
            "is most famous for his paintings, particularly Arrangement in Gray and Black No. 1: "
            "Portrait of the Artist's Mother or Whistler's Mother, as it is more commonly known. "
            "This painting shows a side view of Whistler's mother, dressed in black and posing "
            "against a gray wall. The asymmetrical nature of the portrait, with his mother seated "
            "off-center, is highly characteristic of Whistler's work."
        ),
        "questions": [
            {
                "prompt": "The paragraph preceding this passage most likely discusses",
                "options": {
                    "A": "a survey of eighteenth-century art",
                    "B": "a different American artist",
                    "C": "Whistler's other famous paintings",
                    "D": "European artists",
                },
                "correct_answer": "B",
                "skill": 1,
            },
            {
                "prompt": "Which of the following best describes the information in the passage?",
                "options": {
                    "A": "Several artists are presented.",
                    "B": "One artist's life and works are described.",
                    "C": "Various paintings are contrasted.",
                    "D": "Whistler's family life is outlined.",
                },
                "correct_answer": "B",
                "skill": 3,
            },
            {
                "prompt": "Whistler is considered an American artist because",
                "options": {
                    "A": "he was born in America",
                    "B": "he spent most of his life in America",
                    "C": "he served in the U.S. military",
                    "D": "he created most of his famous art in America",
                },
                "correct_answer": "A",
                "skill": 3,
            },
            {
                "prompt": 'The word "majority" in line 2 is closest in meaning to',
                "options": {"A": "seniority", "B": "maturity", "C": "large pieces", "D": "high percentage"},
                "correct_answer": "D",
                "skill": 9,
            },
            {
                "prompt": "It is implied in the passage that Whistler's family was",
                "options": {
                    "A": "unable to find any work at all in Russia",
                    "B": "highly supportive of his desire to pursue art",
                    "C": "working class",
                    "D": "military",
                },
                "correct_answer": "D",
                "skill": 6,
            },
            {
                "prompt": 'The word "objections" in line 7 is closest in meaning to',
                "options": {"A": "protests", "B": "goals", "C": "agreements", "D": "battles"},
                "correct_answer": "A",
                "skill": 9,
            },
            {
                "prompt": 'In line 8, the "etchings" are',
                "options": {
                    "A": "a type of painting",
                    "B": "the same as a lithograph",
                    "C": "an art form introduced by Whistler",
                    "D": "an art form involving engraving",
                },
                "correct_answer": "D",
                "skill": 4,
            },
            {
                "prompt": 'The word "asymmetrical" in line 11 is closest in meaning to',
                "options": {"A": "proportionate", "B": "uneven", "C": "balanced", "D": "lyrical"},
                "correct_answer": "B",
                "skill": 9,
            },
            {
                "prompt": "Which of the following is NOT true according to the passage?",
                "options": {
                    "A": "Whistler worked with a variety of art forms.",
                    "B": "Whistler's Mother is not the official name of his painting.",
                    "C": "Whistler is best known for his etchings.",
                    "D": "Whistler's Mother is painted in somber tones.",
                },
                "correct_answer": "C",
                "skill": 4,
            },
            {
                "prompt": "Where in the passage does the author mention the types of artwork that Whistler was involved in?",
                "options": {"A": "Lines 1-3", "B": "Lines 4-5", "C": "Lines 6-7", "D": "Lines 8-10"},
                "correct_answer": "C",
                "skill": 12,
            },
        ],
    },
    {
        "key": "stars_fixed",
        "title": "The Movement of Stars",
        "text": (
            "The locations of stars in the sky relative to one another do not appear to the naked "
            "eye to change, and as a result stars are often considered to be fixed in position. "
            "Many unaware stargazers falsely assume that each star has its own permanent home in "
            "the nighttime sky.\n\n"
            "In reality, though, stars are always moving, but because of the tremendous distances "
            "between stars themselves and from stars to Earth, the changes are barely perceptible "
            "here. An example of a rather fast-moving star demonstrates why this misconception "
            "prevails; it takes approximately 200 years for a relatively rapid star like Bernard's "
            "star to move a distance in the skies equal to the diameter of the earth's moon. When "
            "the apparently negligible movement of the stars is contrasted with the movement of the "
            "planets, the stars are seemingly unmoving."
        ),
        "questions": [
            {
                "prompt": "Which of the following is the best title for this passage?",
                "options": {
                    "A": "What the Eye Can See in the Sky",
                    "B": "Bernard's Star",
                    "C": "Planetary Movement",
                    "D": "The Evermoving Stars",
                },
                "correct_answer": "D",
                "skill": 1,
            },
            {
                "prompt": 'The expression "naked eye" in line 1 most probably refers to',
                "options": {
                    "A": "a telescope",
                    "B": "a scientific method for observing stars",
                    "C": "unassisted vision",
                    "D": "a camera with a powerful lens",
                },
                "correct_answer": "C",
                "skill": 11,
            },
            {
                "prompt": "According to the passage, the distances between the stars and Earth are",
                "options": {"A": "barely perceptible", "B": "huge", "C": "fixed", "D": "moderate"},
                "correct_answer": "B",
                "skill": 3,
            },
            {
                "prompt": 'The word "perceptible" in line 5 is closest in meaning to which of the following?',
                "options": {"A": "Noticeable", "B": "Persuasive", "C": "Conceivable", "D": "Astonishing"},
                "correct_answer": "A",
                "skill": 9,
            },
            {
                "prompt": 'In line 6, a "misconception" is closest in meaning to a(n)',
                "options": {"A": "idea", "B": "proven fact", "C": "erroneous belief", "D": "theory"},
                "correct_answer": "C",
                "skill": 9,
            },
            {
                "prompt": "The passage states that in 200 years Bernard's star can move",
                "options": {
                    "A": "around Earth's moon",
                    "B": "next to Earth's moon",
                    "C": "a distance equal to the distance from Earth to the Moon",
                    "D": "a distance seemingly equal to the diameter of the Moon",
                },
                "correct_answer": "D",
                "skill": 3,
            },
            {
                "prompt": "The passage implies that from Earth it appears that the planets",
                "options": {
                    "A": "are fixed in the sky",
                    "B": "move more slowly than the stars",
                    "C": "show approximately the same amount of movement as the stars",
                    "D": "travel through the sky considerably more rapidly than the stars",
                },
                "correct_answer": "D",
                "skill": 6,
            },
            {
                "prompt": 'The word "negligible" in line 8 could most easily be replaced by',
                "options": {"A": "negative", "B": "insignificant", "C": "rapid", "D": "distant"},
                "correct_answer": "B",
                "skill": 11,
            },
            {
                "prompt": "Which of the following is NOT true according to the passage?",
                "options": {
                    "A": "Stars do not appear to the eye to move.",
                    "B": "The large distances between stars and the earth tend to magnify movement to the eye.",
                    "C": "Bernard's star moves quickly in comparison with other stars.",
                    "D": "Although stars move, they seem to be fixed.",
                },
                "correct_answer": "B",
                "skill": 4,
            },
            {
                "prompt": "The paragraph following the passage most probably discusses",
                "options": {
                    "A": "the movement of the planets",
                    "B": "Bernard's star",
                    "C": "the distance from Earth to the Moon",
                    "D": "why stars are always moving",
                },
                "correct_answer": "A",
                "skill": 7,
            },
            {
                "prompt": "This passage would most probably be assigned reading in which course?",
                "options": {"A": "Astrology", "B": "Geophysics", "C": "Astronomy", "D": "Geography"},
                "correct_answer": "C",
                "skill": 13,
            },
        ],
    },
    {
        "key": "no_fault_divorce",
        "title": "No-Fault Divorce",
        "text": (
            "It has been noted that, traditionally, courts have granted divorces on fault grounds: "
            "one spouse is deemed to be at fault in causing the divorce. More and more today, "
            "however, divorces are being granted on a no-fault basis.\n\n"
            "Proponents of no-fault divorce argue that when a marriage fails, it is rarely the case "
            "that one marriage partner is completely to blame and the other blameless. A failed "
            "marriage is much more often the result of mistakes by both partners.\n\n"
            "Another argument in favor of no-fault divorce is that proving fault in court, in a "
            "public arena, is a destructive process that only serves to lengthen the divorce "
            "process and that dramatically increases the negative feelings present in a divorce. "
            "If a couple can reach a decision to divorce without first deciding which partner is to "
            "blame, the divorce settlement can be negotiated more easily and equitably and the "
            "postdivorce healing process can begin more rapidly."
        ),
        "questions": [
            {
                "prompt": "What does the passage mainly discuss?",
                "options": {
                    "A": "Traditional grounds for divorce",
                    "B": "Who is at fault in a divorce",
                    "C": "Why no-fault divorces are becoming more common",
                    "D": "The various reasons for divorces",
                },
                "correct_answer": "C",
                "skill": 1,
            },
            {
                "prompt": 'The word "spouse" in line 1 is closest in meaning to a',
                "options": {"A": "judge", "B": "problem", "C": "divorce decree", "D": "marriage partner"},
                "correct_answer": "D",
                "skill": 9,
            },
            {
                "prompt": "According to the passage, no-fault divorces",
                "options": {
                    "A": "are on the increase",
                    "B": "are the traditional form of divorce",
                    "C": "are less popular than they used to be",
                    "D": "were granted more in the past",
                },
                "correct_answer": "A",
                "skill": 3,
            },
            {
                "prompt": "It is implied in the passage that",
                "options": {
                    "A": "there recently has been a decrease in no-fault divorces",
                    "B": "not all divorces today are no-fault divorces",
                    "C": "a no-fault divorce is not as equitable as a fault divorce",
                    "D": "people recover more slowly from a no-fault divorce",
                },
                "correct_answer": "B",
                "skill": 6,
            },
            {
                "prompt": 'The word "Proponents" in line 4 is closest in meaning to which of the following?',
                "options": {"A": "Advocates", "B": "Recipients", "C": "Authorities", "D": "Enemies"},
                "correct_answer": "A",
                "skill": 9,
            },
            {
                "prompt": "The passage states that a public trial to prove the fault of one spouse can",
                "options": {
                    "A": "be satisfying to the wronged spouse",
                    "B": "lead to a shorter divorce process",
                    "C": "reduce negative feelings",
                    "D": "be a harmful process",
                },
                "correct_answer": "D",
                "skill": 3,
            },
            {
                "prompt": "Which of the following is NOT listed in this passage as an argument in favor of no-fault divorce?",
                "options": {
                    "A": "Rarely is only one marriage partner to blame for a divorce.",
                    "B": "A no-fault divorce generally costs less in legal fees.",
                    "C": "Finding fault in a divorce increases negative feelings.",
                    "D": "A no-fault divorce settlement is generally easier to negotiate.",
                },
                "correct_answer": "B",
                "skill": 4,
            },
            {
                "prompt": 'The word "present" in line 9 could most easily be replaced by',
                "options": {"A": "existing", "B": "giving", "C": "introducing", "D": "resulting"},
                "correct_answer": "A",
                "skill": 11,
            },
            {
                "prompt": 'The word "settlement" in line 10 is closest in meaning to',
                "options": {"A": "development", "B": "serenity", "C": "discussion", "D": "agreement"},
                "correct_answer": "D",
                "skill": 9,
            },
            {
                "prompt": "The tone of this passage is",
                "options": {"A": "emotional", "B": "enthusiastic", "C": "expository", "D": "reactionary"},
                "correct_answer": "C",
                "skill": 13,
            },
        ],
    },
    {
        "key": "revolutionary_literature",
        "title": "American Literature in the Revolutionary Era",
        "text": (
            "Whereas literature in the first half of the eighteenth century in America had been "
            "largely religious and moral in tone, by the latter half of the century the "
            "revolutionary fervor that was coming to life in the colonies began to be reflected in "
            "the literature of the time, which in turn served to further influence the population. "
            "Although not all writers of this period supported the Revolution, the two best-known "
            "and most influential writers, Ben Franklin and Thomas Paine, were both strongly "
            "supportive of that cause.\n\n"
            "Ben Franklin first attained popular success through his writings in his brother's "
            "newspaper, the New England Current. In these articles he used a simple style of "
            "language and common sense argumentation to defend the point of view of the farmer and "
            "the Leather Apron man. He continued with the same common sense practicality and appeal "
            "to the common man with his work on Poor Richard's Almanac from 1733 until 1758. Firmly "
            "established in his popular acceptance by the people, Franklin wrote a variety of "
            "extremely effective articles and pamphlets about the colonists' revolutionary cause "
            "against England.\n\n"
            "Thomas Paine was an Englishman working as a magazine editor in Philadelphia at the "
            "time of the Revolution. His pamphlet Common Sense, which appeared in 1776, was a force "
            "in encouraging the colonists to declare their independence from England. Then "
            "throughout the long and desperate war years he published a series of Crisis papers "
            "(from 1776 until 1783) to encourage the colonists to continue on with the struggle. "
            "The effectiveness of his writing was probably due to his emotional yet oversimplified "
            "depiction of the cause of the colonists against England as a classic struggle of good "
            "and evil."
        ),
        "questions": [
            {
                "prompt": "The paragraph preceding this passage most likely discusses",
                "options": {
                    "A": "how literature influences the population",
                    "B": "religious and moral literature",
                    "C": "literature supporting the cause of the American Revolution",
                    "D": "what made Thomas Paine's literature successful",
                },
                "correct_answer": "B",
                "skill": 1,
            },
            {
                "prompt": 'The word "fervor" in line 2 is closest in meaning to',
                "options": {"A": "war", "B": "anxiety", "C": "spirit", "D": "action"},
                "correct_answer": "C",
                "skill": 9,
            },
            {
                "prompt": 'The word "time" in line 3 could best be replaced by',
                "options": {"A": "hour", "B": "period", "C": "appointment", "D": "duration"},
                "correct_answer": "B",
                "skill": 11,
            },
            {
                "prompt": "It is implied in the passage that",
                "options": {
                    "A": "some writers in the American colonies supported England during the Revolution",
                    "B": "Franklin and Paine were the only writers to influence the Revolution",
                    "C": "because Thomas Paine was an Englishman, he supported England against the colonies",
                    "D": "authors who supported England did not remain in the colonies during the Revolution",
                },
                "correct_answer": "A",
                "skill": 6,
            },
            {
                "prompt": 'The pronoun "he" in line 8 refers to',
                "options": {"A": "Thomas Paine", "B": "Ben Franklin", "C": "Ben Franklin's brother", "D": "Poor Richard"},
                "correct_answer": "B",
                "skill": 5,
            },
            {
                "prompt": 'The expression "point of view" in line 9 could best be replaced by',
                "options": {"A": "perspective", "B": "sight", "C": "circumstance", "D": "trait"},
                "correct_answer": "A",
                "skill": 11,
            },
            {
                "prompt": "According to the passage, the tone of Poor Richard's Almanac is",
                "options": {"A": "pragmatic", "B": "erudite", "C": "theoretical", "D": "scholarly"},
                "correct_answer": "A",
                "skill": 3,
            },
            {
                "prompt": 'The word "desperate" in line 16 could best be replaced by',
                "options": {"A": "unending", "B": "hopeless", "C": "strategic", "D": "combative"},
                "correct_answer": "B",
                "skill": 10,
            },
            {
                "prompt": "Where in the passage does the author describe Thomas Paine's style of writing?",
                "options": {"A": "Lines 4-6", "B": "Lines 8-9", "C": "Lines 14-15", "D": "Lines 18-20"},
                "correct_answer": "D",
                "skill": 12,
            },
            {
                "prompt": "The purpose of the passage is to",
                "options": {
                    "A": "discuss American literature in the first half of the eighteenth century",
                    "B": "give biographical data on two American writers",
                    "C": "explain which authors supported the Revolution",
                    "D": "describe the literary influence during revolutionary America",
                },
                "correct_answer": "D",
                "skill": 13,
            },
        ],
    },
]


def get_or_create_skill(session: Session, number: int) -> Skill:
    skill = session.exec(
        select(Skill).where(Skill.section == Section.reading, Skill.number == number)
    ).first()
    if skill is None:
        skill = Skill(section=Section.reading, number=number)
        session.add(skill)
        session.commit()
        session.refresh(skill)
    return skill


def seed() -> None:
    with Session(engine) as session:
        inserted = 0
        for passage_data in PASSAGES:
            passage = Passage(
                title=passage_data["title"],
                text=passage_data["text"],
                source=SOURCE,
            )
            session.add(passage)
            session.commit()
            session.refresh(passage)

            for item in passage_data["questions"]:
                question = Question(
                    section=Section.reading,
                    question_type=QuestionType.multiple_choice,
                    prompt=item["prompt"],
                    options=item["options"],
                    correct_answer=item["correct_answer"],
                    verified=False,
                    passage_id=passage.id,
                    source=SOURCE,
                )
                question.skills = [get_or_create_skill(session, item["skill"])]
                session.add(question)
                inserted += 1

        session.commit()
        print(f"{inserted} preguntas de Reading insertadas en {len(PASSAGES)} passages.")


if __name__ == "__main__":
    seed()
