"""
Carga a la base de datos las preguntas de Structure y Written Expression
del "Exam 1" extraidas de TOEFL_tests_2026.pdf (paginas 185-191).

IMPORTANTE sobre las respuestas correctas:
El PDF fuente incluye la tabla "pregunta -> skill" para autoevaluacion,
pero NO incluye una hoja de respuestas correctas (esa pagina no fue
extraida). Las respuestas de este archivo fueron determinadas mediante
analisis gramatical de cada oracion -- por eso toda pregunta se carga
con verified=False. Si en algun momento se consigue el answer key oficial
del libro, se debe correr un script de verificacion que compare y
actualice verified=True donde coincida.

Uso:
    python scripts/seed_exam1_structure.py
"""
from sqlmodel import Session, select

from app.core.database import engine
from app.modules.question_bank.models import Question, QuestionType, Section, Skill

SOURCE = "TOEFL_tests_2026.pdf - Exam 1 Structure and Written Expression (p.185-191)"

# --- Structure (sentence completion): 15 preguntas ---
STRUCTURE_QUESTIONS = [
    {
        "prompt": "The North Pole ___ a latitude of 90 degrees north.",
        "options": {"A": "it has", "B": "is having", "C": "which is having", "D": "has"},
        "correct_answer": "D",
        "skills": [1],
    },
    {
        "prompt": "The city of Beverly Hills is surrounded on ___ the city of Los Angeles.",
        "options": {"A": "its sides", "B": "the sides are", "C": "it is the side of", "D": "all sides by"},
        "correct_answer": "D",
        "skills": [2],
    },
    {
        "prompt": "___ greyhound, can achieve speeds up to thirty-six miles per hour.",
        "options": {"A": "The", "B": "The fastest", "C": "The fastest dog", "D": "The fastest dog, the"},
        "correct_answer": "D",
        "skills": [3],
    },
    {
        "prompt": "Marmots spend their time foraging among meadow plants and flowers or ___ on rocky cliffs.",
        "options": {"A": "gets sun", "B": "sunning", "C": "the sun", "D": "sunny"},
        "correct_answer": "B",
        "skills": [6],
    },
    {
        "prompt": "The greenhouse effect occurs ___ heat radiated from the Sun.",
        "options": {
            "A": "when does the Earth's atmosphere trap",
            "B": "does the Earth's atmosphere trap",
            "C": "when the Earth's atmosphere traps",
            "D": "the Earth's atmosphere traps",
        },
        "correct_answer": "C",
        "skills": [7, 15],
    },
    {
        "prompt": (
            "The Rose Bowl, ___ place on New Year's Day, is the oldest postseason "
            "collegiate football game in the United States."
        ),
        "options": {"A": "takes", "B": "it takes", "C": "which takes", "D": "took"},
        "correct_answer": "C",
        "skills": [12],
    },
    {
        "prompt": "Experiments ___ represent a giant step into the medicine of the future.",
        "options": {
            "A": "using gene therapy",
            "B": "use gene therapy",
            "C": "they use",
            "D": "gene therapy uses",
        },
        "correct_answer": "A",
        "skills": [4, 13],
    },
    {
        "prompt": "___ off the Hawaiian coastline are living, others are dead.",
        "options": {
            "A": "While some types of coral reefs",
            "B": "Some types of coral reefs",
            "C": "There are many types of coral reefs",
            "D": "Coral reefs",
        },
        "correct_answer": "A",
        "skills": [8],
    },
    {
        "prompt": "Nimbostratus clouds are thick, dark gray clouds ___ forebode rain.",
        "options": {"A": "what", "B": "which", "C": "what they", "D": "which they"},
        "correct_answer": "B",
        "skills": [12],
    },
    {
        "prompt": (
            "Some economists now suggest that home equity loans are merely a new "
            "trap to push consumers beyond ___."
        ),
        "options": {
            "A": "they can afford",
            "B": "they can afford it",
            "C": "what is affordable",
            "D": "able to afford",
        },
        "correct_answer": "C",
        "skills": [10],
    },
    {
        "prompt": "People who reverse the letters of words ___ to read suffer from dyslexia.",
        "options": {"A": "when trying", "B": "if they tried", "C": "when tried", "D": "if he tries"},
        "correct_answer": "A",
        "skills": [14],
    },
    {
        "prompt": "Featured at the Henry Ford Museum ___ of antique cars dating from 1865.",
        "options": {"A": "is an exhibit", "B": "an exhibit", "C": "an exhibit is", "D": "which is an exhibit"},
        "correct_answer": "A",
        "skills": [16],
    },
    {
        "prompt": (
            "Rubber ___ from vulcanized silicones with a high molecular weight is "
            "difficult to distinguish from natural rubber."
        ),
        "options": {"A": "is produced", "B": "producing", "C": "that produces", "D": "produced"},
        "correct_answer": "D",
        "skills": [5, 13],
    },
    {
        "prompt": (
            "___ appears considerably larger at the horizon than it does overhead "
            "is merely an optical illusion."
        ),
        "options": {"A": "The Moon", "B": "That the Moon", "C": "When the Moon", "D": "The Moon which"},
        "correct_answer": "B",
        "skills": [9],
    },
    {
        "prompt": (
            "According to the World Health Organization, ___ any of the six most "
            "dangerous diseases to break out, it could be cause for quarantine."
        ),
        "options": {"A": "were", "B": "they were", "C": "there were", "D": "were they"},
        "correct_answer": "A",
        "skills": [18],
    },
]

# --- Written Expression (error identification): 25 preguntas ---
WRITTEN_EXPRESSION_QUESTIONS = [
    {
        "prompt": (
            "On the floor of the Pacific Ocean {A}is{A} hundreds of flat-topped "
            "mountains {B}more than a{B} mile beneath sea level."
        ),
        "options": {
            "A": "the floor of the Pacific Ocean",
            "B": "is",
            "C": "flat-topped",
            "D": "more than a",
        },
        "correct_answer": "B",
        "explanation": "El sujeto real es 'hundreds of...mountains' (plural); el verbo debe ser 'are', no 'is'.",
        "skills": [22],
    },
    {
        "prompt": (
            "Because of the flourish with which John Hancock signed the "
            "Declaration of Independence, his name become synonymous with signature."
        ),
        "options": {
            "A": "with which",
            "B": "become",
            "C": "synonymous",
            "D": "with signature",
        },
        "correct_answer": "B",
        "explanation": "Se necesita el pasado 'became', no la forma base 'become'.",
        "skills": [33],
    },
    {
        "prompt": "Segregation in public schools was declare unconstitutional by the Supreme Court in 1954.",
        "options": {
            "A": "Segregation in public schools",
            "B": "was declare",
            "C": "unconstitutional",
            "D": "in 1954",
        },
        "correct_answer": "B",
        "explanation": "Voz pasiva: debe ser 'was declared', con el participio.",
        "skills": [31],
    },
    {
        "prompt": (
            "Sirius, the Dog Star, is the most brightest star in the sky with an "
            "absolute magnitude about twenty-three times that of the Sun."
        ),
        "options": {
            "A": "the most brightest star",
            "B": "an absolute magnitude",
            "C": "about twenty-three times",
            "D": "that",
        },
        "correct_answer": "A",
        "explanation": "Doble superlativo incorrecto: debe ser solo 'the brightest star'.",
        "skills": [27],
    },
    {
        "prompt": "Killer whales tend to wander in family clusters that hunt, play, and resting together.",
        "options": {"A": "tend", "B": "to wander", "C": "hunt, play, and", "D": "resting"},
        "correct_answer": "D",
        "explanation": "Estructura paralela: 'hunt, play, and rest', no 'resting'.",
        "skills": [24],
    },
    {
        "prompt": "Some of the most useful resistor material are carbon, metals, and metallic alloys.",
        "options": {
            "A": "Some of the most useful resistor",
            "B": "material",
            "C": "are",
            "D": "metallic",
        },
        "correct_answer": "B",
        "explanation": "El verbo plural 'are' exige el sustantivo en plural: 'materials'.",
        "skills": [21],
    },
    {
        "prompt": "The community of Bethesda, Maryland, was previous known as Darcy's Store.",
        "options": {
            "A": "The community of Bethesda, Maryland,",
            "B": "previous",
            "C": "known",
            "D": "as Darcy's Store",
        },
        "correct_answer": "B",
        "explanation": "Se necesita el adverbio 'previously' para modificar 'known', no el adjetivo 'previous'.",
        "skills": [47],
    },
    {
        "prompt": "Alloys of gold and copper have been widely using in various types of coins.",
        "options": {
            "A": "Alloys of gold and copper",
            "B": "have been widely",
            "C": "using",
            "D": "in various types of",
        },
        "correct_answer": "C",
        "explanation": "Voz pasiva perfecta: 'have been widely used', no 'using'.",
        "skills": [51],
    },
    {
        "prompt": (
            "J. H. Pratt used group therapy early in this century when he brought "
            "tuberculosis patients together to discuss its disease."
        ),
        "options": {
            "A": "used group therapy",
            "B": "early in this century",
            "C": "when he brought",
            "D": "its disease",
        },
        "correct_answer": "D",
        "explanation": "El pronombre debe concordar con 'patients' (plural): 'their disease', no 'its'.",
        "skills": [45],
    },
    {
        "prompt": (
            "The United States has import all carpet wools in recent years because "
            "domestic wools are too fine and soft for carpets."
        ),
        "options": {
            "A": "The United States has",
            "B": "import",
            "C": "because",
            "D": "too fine and soft",
        },
        "correct_answer": "B",
        "explanation": "Presente perfecto: 'has imported', no 'has import'.",
        "skills": [30],
    },
    {
        "prompt": (
            'Irving Berlin wrote "Oh How I Hate to Get Up in the Morning" while '
            "serving in a U.S. Army during World War I."
        ),
        "options": {
            "A": "wrote",
            "B": "while serving",
            "C": "in a",
            "D": "U.S. Army",
        },
        "correct_answer": "C",
        "explanation": "Instituciones como 'the U.S. Army' llevan artículo definido, no 'a'.",
        "skills": [51],
    },
    {
        "prompt": "Banks are rushing to merge because consolidations enable them to slash theirs costs and expand.",
        "options": {
            "A": "are rushing to merge",
            "B": "enable them",
            "C": "theirs",
            "D": "expand",
        },
        "correct_answer": "C",
        "explanation": "Se necesita el adjetivo posesivo 'their', no el pronombre posesivo 'theirs'.",
        "skills": [44],
    },
    {
        "prompt": (
            "That water has a very high specific heat means that without a large "
            "temperature change water can add or lose a large number of heat."
        ),
        "options": {
            "A": "That water has",
            "B": "means",
            "C": "can add or lose",
            "D": "number",
        },
        "correct_answer": "D",
        "explanation": "'Heat' es incontable: se usa 'amount of heat', no 'number of heat'.",
        "skills": [40],
    },
    {
        "prompt": (
            "Benny Goodman was equally talented as both a jazz performer as well "
            "as a classical musician."
        ),
        "options": {
            "A": "equally",
            "B": "performer",
            "C": "as well as",
            "D": "classical musician",
        },
        "correct_answer": "C",
        "explanation": "Redundante junto con 'both': debe ser 'both...and', no 'both...as well as'.",
        "skills": [25],
    },
    {
        "prompt": (
            "The state seal still used in Massachusetts designed by Paul Revere, "
            "who also designed the first Continental currency."
        ),
        "options": {
            "A": "still used",
            "B": "designed by",
            "C": "who also designed",
            "D": "the first",
        },
        "correct_answer": "B",
        "explanation": "Falta el verbo principal de la oración: debe ser 'was designed by'.",
        "skills": [37],
    },
    {
        "prompt": (
            "Quarter horses were developed in eighteenth-century Virginia to race "
            "on courses short of about a quarter of a mile in length."
        ),
        "options": {
            "A": "were developed",
            "B": "courses short",
            "C": "of a mile",
            "D": "in length",
        },
        "correct_answer": "B",
        "explanation": "Orden de palabras: debe ser 'short courses', adjetivo antes del sustantivo.",
        "skills": [48],
    },
    {
        "prompt": (
            "No longer satisfied with the emphasis of the Denishawn School, Martha "
            "Graham has moved to the staff of the Eastman School in 1925."
        ),
        "options": {
            "A": "No longer satisfied",
            "B": "the emphasis",
            "C": "Martha Graham",
            "D": "has moved",
        },
        "correct_answer": "D",
        "explanation": "Con una fecha específica pasada ('in 1925') se usa pasado simple 'moved', no presente perfecto.",
        "skills": [35],
    },
    {
        "prompt": "William Hart was an act best known for his roles as western heroes in silent films.",
        "options": {
            "A": "an act",
            "B": "best known",
            "C": "his roles",
            "D": "in silent films",
        },
        "correct_answer": "A",
        "explanation": "Debe ser el sustantivo de persona 'an actor', no 'an act'.",
        "skills": [42],
    },
    {
        "prompt": (
            "Prior to an extermination program earlier this century, alive wolves "
            "roamed across nearly all of North America."
        ),
        "options": {
            "A": "Prior to",
            "B": "earlier this century",
            "C": "alive",
            "D": "roamed",
        },
        "correct_answer": "C",
        "explanation": "'Alive' no se usa antes del sustantivo (atributivo); debe ser 'living wolves'.",
        "skills": [50],
    },
    {
        "prompt": (
            "During the 1960s the Berkeley campus of the University of California "
            "came to national attention as a result its radical political activity."
        ),
        "options": {
            "A": "During the 1960s",
            "B": "came to",
            "C": "a result",
            "D": "radical political",
        },
        "correct_answer": "C",
        "explanation": "Falta la preposición: debe ser 'as a result of its radical political activity'.",
        "skills": [57],
    },
    {
        "prompt": (
            "Artist Gutzon Borglum designed the Mount Rushmore Memorial and worked "
            "on project from 1925 until his death in 1941."
        ),
        "options": {
            "A": "Artist",
            "B": "project",
            "C": "from 1925 until",
            "D": "his death",
        },
        "correct_answer": "B",
        "explanation": "Falta el artículo: debe ser 'worked on the project'.",
        "skills": [52],
    },
    {
        "prompt": "It is proving less costly and more profitably for drugmakers to market directly to patients.",
        "options": {
            "A": "less costly",
            "B": "more profitably",
            "C": "for drugmakers",
            "D": "directly to",
        },
        "correct_answer": "B",
        "explanation": "Estructura paralela con 'less costly': debe ser el adjetivo 'more profitable', no el adverbio.",
        "skills": [47, 49],
    },
    {
        "prompt": "Sapphires weighing as much as two pounds have on occasion mined.",
        "options": {
            "A": "weighing",
            "B": "as much as",
            "C": "have on occasion",
            "D": "mined",
        },
        "correct_answer": "D",
        "explanation": "Falta el auxiliar 'been' de la voz pasiva perfecta: 'have on occasion been mined'.",
        "skills": [38],
    },
    {
        "prompt": "Like snakes, lizards can be found on all others continents except Antarctica.",
        "options": {
            "A": "Like snakes",
            "B": "can be found",
            "C": "others",
            "D": "except",
        },
        "correct_answer": "C",
        "explanation": "Debe ser el adjetivo 'other continents', no 'others continents'.",
        "skills": [60],
    },
    {
        "prompt": (
            "Banks, savings and loans, and finance companies have recently been "
            "doing home equity loans with greater frequency than ever before."
        ),
        "options": {
            "A": "Banks, savings and loans,",
            "B": "have recently been",
            "C": "doing",
            "D": "greater frequency",
        },
        "correct_answer": "C",
        "explanation": "Colocación idiomática: se dice 'making loans', no 'doing loans'.",
        "skills": [58],
    },
]


def get_or_create_skill(session: Session, section: Section, number: int) -> Skill:
    skill = session.exec(
        select(Skill).where(Skill.section == section, Skill.number == number)
    ).first()
    if skill is None:
        skill = Skill(section=section, number=number)
        session.add(skill)
        session.commit()
        session.refresh(skill)
    return skill


def seed() -> None:
    with Session(engine) as session:
        inserted = 0
        for item in STRUCTURE_QUESTIONS:
            question = Question(
                section=Section.structure,
                question_type=QuestionType.sentence_completion,
                prompt=item["prompt"],
                options=item["options"],
                correct_answer=item["correct_answer"],
                verified=False,
                explanation=item.get("explanation"),
                source=SOURCE,
            )
            question.skills = [get_or_create_skill(session, Section.structure, n) for n in item["skills"]]
            session.add(question)
            inserted += 1

        for item in WRITTEN_EXPRESSION_QUESTIONS:
            question = Question(
                section=Section.written_expression,
                question_type=QuestionType.error_identification,
                prompt=item["prompt"],
                options=item["options"],
                correct_answer=item["correct_answer"],
                verified=False,
                explanation=item.get("explanation"),
                source=SOURCE,
            )
            question.skills = [get_or_create_skill(session, Section.written_expression, n) for n in item["skills"]]
            session.add(question)
            inserted += 1

        session.commit()
        print(f"{inserted} preguntas insertadas ({len(STRUCTURE_QUESTIONS)} structure + "
              f"{len(WRITTEN_EXPRESSION_QUESTIONS)} written expression).")


if __name__ == "__main__":
    seed()
