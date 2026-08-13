"""
Carga las preguntas de Structure y Written Expression del PRE-TEST
extraidas de LONGMAN_INTRODUCTORY_COURSE_PART2_PART3.pdf (paginas 55-60).

Mismas advertencias que los seeds anteriores: verified=False. Este
pre-test tampoco trae tabla de skills en el material extraido -> sin skills.

Uso:
    python -m scripts.seed_longman_structure_pretest
"""
from sqlmodel import Session

from app.core.database import engine
from app.modules.question_bank.models import Question, QuestionType, Section

SOURCE = "LONGMAN_INTRODUCTORY_COURSE_PART2_PART3.pdf - Structure and Written Expression Pre-Test (p.55-60)"

STRUCTURE_QUESTIONS = [
    {
        "prompt": "In the early 1900s, Eastman ___ inexpensive Brownie box cameras.",
        "options": {"A": "it developed", "B": "it was developed", "C": "developed", "D": "developing"},
        "correct_answer": "C",
    },
    {
        "prompt": "___ the discovery of the fossilized remnants of tides in one-billion-year-old rocks.",
        "options": {
            "A": "Geological reports",
            "B": "Geologists report",
            "C": "The reports of geologists",
            "D": "Geologists' reports",
        },
        "correct_answer": "B",
    },
    {
        "prompt": "The Brooklyn Bridge ___ took thirteen years to complete.",
        "options": {"A": "in New York", "B": "is in New York", "C": "it is in New York", "D": "which New York"},
        "correct_answer": "A",
    },
    {
        "prompt": "Genes control all of the physical ___ we inherit.",
        "options": {"A": "that traits", "B": "that are traits", "C": "traits that", "D": "traits are that"},
        "correct_answer": "C",
    },
    {
        "prompt": "Indigo can be extracted from a plant, and then ___ to dye cloth blue.",
        "options": {"A": "it", "B": "using", "C": "using it", "D": "it can be used"},
        "correct_answer": "D",
    },
    {
        "prompt": (
            "___ in the United States spends 900 hours per year in class and 1,170 "
            "hours in front of the television."
        ),
        "options": {
            "A": "The average third-grader",
            "B": "The third grade is average",
            "C": "There are three grades",
            "D": "Three average grades",
        },
        "correct_answer": "A",
    },
    {
        "prompt": "Researchers have begun studying what ___ is on human circadian rhythms.",
        "options": {
            "A": "it is the effect of light",
            "B": "the light affects",
            "C": "is affecting the light",
            "D": "the effect of light",
        },
        "correct_answer": "D",
    },
    {
        "prompt": "If calcium oxide remains exposed to air, ___ to calcium carbonate.",
        "options": {"A": "turning", "B": "turns", "C": "it turns", "D": "the turn"},
        "correct_answer": "C",
    },
    {
        "prompt": "Some early batteries used concentrated nitric acid, ___ gave off poisonous fumes.",
        "options": {"A": "they", "B": "then they", "C": "but they", "D": "but they had"},
        "correct_answer": "C",
    },
    {
        "prompt": (
            "The sound produced by an object ___ in a periodic way involves more "
            "than the simple sine wave."
        ),
        "options": {"A": "it vibrates", "B": "vibrating", "C": "is vibrating", "D": "vibrates"},
        "correct_answer": "B",
    },
    {
        "prompt": "Prior to the discovery of anesthetics in 1846, surgery was done ___ was still conscious.",
        "options": {"A": "while the patient", "B": "the patient felt", "C": "during the patient's", "D": "while patiently"},
        "correct_answer": "A",
    },
    {
        "prompt": (
            "The drastic decline of the beaver helps to illustrate what ___ to the "
            "ecosystems of the North American continent."
        ),
        "options": {"A": "happening", "B": "the happening", "C": "has happened", "D": "about happening"},
        "correct_answer": "C",
    },
    {
        "prompt": "The use of shorthand died out in the Middle Ages because of ___ with witchcraft.",
        "options": {
            "A": "the association was imagined",
            "B": "associate the imagination",
            "C": "imagine the association",
            "D": "the imagined association",
        },
        "correct_answer": "D",
    },
    {
        "prompt": "A yacht is steered with a rudder, ___ the flow of water that passes the hull.",
        "options": {"A": "which deflecting", "B": "deflects", "C": "it deflects", "D": "which deflects"},
        "correct_answer": "D",
    },
    {
        "prompt": (
            "For top speed and sudden acceleration, the accelerator pump feeds "
            "additional gasoline from the float chamber into ___ above the venturi tube."
        ),
        "options": {"A": "the air flows", "B": "the air flow", "C": "the air is flowing", "D": "flows the air"},
        "correct_answer": "B",
    },
]

WRITTEN_EXPRESSION_QUESTIONS = [
    {
        "prompt": "In 1732, coach travelers could got from New York to Philadelphia in about two days.",
        "options": {"A": "In 1732", "B": "coach travelers", "C": "could got", "D": "in about two days"},
        "correct_answer": "C",
        "explanation": "Después de un modal se usa la forma base del verbo: 'could get', no 'could got'.",
    },
    {
        "prompt": "Some of the District of Columbia are on low-lying, marshy ground.",
        "options": {"A": "Some of", "B": "the District of Columbia", "C": "are", "D": "low-lying, marshy"},
        "correct_answer": "C",
        "explanation": "'The District of Columbia' es una entidad singular: el verbo debe ser 'is', no 'are'.",
    },
    {
        "prompt": "Georgia's economy is based main on agriculture.",
        "options": {"A": "Georgia's economy", "B": "is based", "C": "main", "D": "on agriculture"},
        "correct_answer": "C",
        "explanation": "Se necesita el adverbio 'mainly' para modificar 'based', no el adjetivo 'main'.",
    },
    {
        "prompt": "The Paul Revere House was built in 1676, and today its the oldest wooden building in Boston.",
        "options": {"A": "was built", "B": "and today", "C": "its", "D": "oldest wooden building"},
        "correct_answer": "C",
        "explanation": "Se necesita la contracción 'it's' (it is), no el posesivo 'its'.",
    },
    {
        "prompt": "Conifers such as cedars, firs, and pines bear its seeds in cones.",
        "options": {"A": "such as", "B": "bear", "C": "its", "D": "in cones"},
        "correct_answer": "C",
        "explanation": "El pronombre debe concordar con 'Conifers' (plural): 'their seeds', no 'its'.",
    },
    {
        "prompt": "A dome is a semispherical structures on top of a building.",
        "options": {"A": "A dome is a", "B": "semispherical structures", "C": "on top", "D": "of a building"},
        "correct_answer": "B",
        "explanation": "Con el artículo singular 'a' se necesita el sustantivo en singular: 'structure', no 'structures'.",
    },
    {
        "prompt": "Succulents suck up water in just a few hour, but they can store it in their stems for months.",
        "options": {"A": "suck up", "B": "in just a few hour", "C": "they can store", "D": "in their stems"},
        "correct_answer": "B",
        "explanation": "Con 'a few' se necesita el plural: 'a few hours', no 'a few hour'.",
    },
    {
        "prompt": "Flying buttresses enabled builders to put up tall but thinnest stone walls.",
        "options": {"A": "Flying buttresses", "B": "enabled", "C": "to put up tall but", "D": "thinnest"},
        "correct_answer": "D",
        "explanation": "Paralelismo con el adjetivo simple 'tall': debe ser 'thin', no el superlativo 'thinnest'.",
    },
    {
        "prompt": "Weather forecasters monitor barometric pressures and record they on charts as isobars.",
        "options": {"A": "monitor", "B": "and record", "C": "they", "D": "as isobars"},
        "correct_answer": "C",
        "explanation": "Se necesita el pronombre objeto 'them', no el pronombre sujeto 'they'.",
    },
    {
        "prompt": (
            "In many languages, the forms of a word varies to express such "
            "contrasts as number, gender, and tense."
        ),
        "options": {"A": "In many languages", "B": "the forms of a word", "C": "varies", "D": "such contrasts as"},
        "correct_answer": "C",
        "explanation": "El sujeto 'the forms' es plural: el verbo debe ser 'vary', no 'varies'.",
    },
    {
        "prompt": (
            "A Milky Way object that erupted in the constellation Scorpius has "
            "provides information to astronomers since July."
        ),
        "options": {"A": "that erupted", "B": "has provides", "C": "information to", "D": "since July"},
        "correct_answer": "B",
        "explanation": "Presente perfecto: debe ser 'has provided', no 'has provides'.",
    },
    {
        "prompt": "Much fossils are found in coal-bearing rocks.",
        "options": {"A": "Much", "B": "fossils", "C": "are found", "D": "coal-bearing"},
        "correct_answer": "A",
        "explanation": "'Fossils' es contable en plural: se usa 'Many fossils', no 'Much fossils'.",
    },
    {
        "prompt": "When salt is added to ice, this mixture becomes coldly enough to freeze ice cream.",
        "options": {"A": "is added", "B": "this mixture", "C": "coldly enough", "D": "to freeze"},
        "correct_answer": "C",
        "explanation": "Después de 'becomes' se necesita el adjetivo 'cold', no el adverbio 'coldly'.",
    },
    {
        "prompt": (
            "During the eighteenth and nineteenth centuries, Long Island was "
            "chiefly an agricultural region with fishing, whaling, and build ships "
            "as the important industries."
        ),
        "options": {
            "A": "During the eighteenth",
            "B": "chiefly an agricultural",
            "C": "with fishing, whaling, and",
            "D": "build ships",
        },
        "correct_answer": "D",
        "explanation": "Estructura paralela con 'fishing, whaling': debe ser el sustantivo 'shipbuilding', no la frase verbal 'build ships'.",
    },
    {
        "prompt": (
            "No one who has studied the Battle of Little Bighorn know the exact "
            "route that Custer and his detachment took."
        ),
        "options": {"A": "who has studied", "B": "know", "C": "the exact route", "D": "took"},
        "correct_answer": "B",
        "explanation": "El sujeto 'No one' es singular: el verbo debe ser 'knows', no 'know'.",
    },
    {
        "prompt": "The folktales which the brothers Grimm had collecting were translated into English in 1823.",
        "options": {"A": "which", "B": "had collecting", "C": "were translated", "D": "into English"},
        "correct_answer": "B",
        "explanation": "El pasado perfecto requiere el participio: 'had collected', no 'had collecting'.",
    },
    {
        "prompt": (
            "In our solar system, nine planets, fifty-seven moons, several dozen "
            "comets, several million asteroids, and billions of meteorites have so "
            "far been discover."
        ),
        "options": {"A": "In our", "B": "several dozen", "C": "several million", "D": "been discover"},
        "correct_answer": "D",
        "explanation": "Después de 'been' se necesita el participio pasado: 'discovered', no 'discover'.",
    },
    {
        "prompt": (
            "From the 1850s until after the turn of the century, many of America's "
            "super-rich families made Newport his favorite summer resort."
        ),
        "options": {"A": "From the 1850s", "B": "many of", "C": "made Newport", "D": "his favorite summer resort"},
        "correct_answer": "D",
        "explanation": "El pronombre debe concordar con 'families' (plural): 'their favorite summer resort', no 'his'.",
    },
    {
        "prompt": "Mars may looks red because it is covered with a layer of soft red iron oxide.",
        "options": {"A": "may looks", "B": "because", "C": "is covered", "D": "soft red"},
        "correct_answer": "A",
        "explanation": "Después de un modal se usa la forma base: 'may look', no 'may looks'.",
    },
    {
        "prompt": (
            "The radioactive substances that pose the greatest harm to humanity "
            "have neither very short or very long half lives."
        ),
        "options": {"A": "that pose", "B": "very short", "C": "or", "D": "half lives"},
        "correct_answer": "C",
        "explanation": "La pareja correcta es 'neither...nor', no 'neither...or'.",
    },
    {
        "prompt": "A robin cocks its head to peer at a worm with one eyes and not to hear it, as was once thought.",
        "options": {"A": "cocks its head", "B": "with one eyes", "C": "and not to hear", "D": "as was once thought"},
        "correct_answer": "B",
        "explanation": "'One' requiere el sustantivo singular: 'one eye', no 'one eyes'.",
    },
    {
        "prompt": "Film sound is often record by an analog system which, like the compact disc, uses light.",
        "options": {"A": "is often record", "B": "an analog system", "C": "which, like", "D": "uses light"},
        "correct_answer": "A",
        "explanation": "Voz pasiva: debe ser 'is often recorded', no 'is often record'.",
    },
    {
        "prompt": "The scribes of the Middle Ages used quill pens to produce their high decorated manuscripts.",
        "options": {"A": "The scribes", "B": "used quill pens", "C": "to produce", "D": "high decorated"},
        "correct_answer": "D",
        "explanation": "Se necesita el adverbio 'highly' para modificar 'decorated', no el adjetivo 'high'.",
    },
    {
        "prompt": (
            "The principles of physics described by Christian Doppler in 1842 for "
            "the movement of stars has been adapted to evaluate the movement of "
            "blood within the heart."
        ),
        "options": {"A": "described by", "B": "for the movement", "C": "has been adapted", "D": "within the heart"},
        "correct_answer": "C",
        "explanation": "El sujeto 'The principles' es plural: debe ser 'have been adapted', no 'has been adapted'.",
    },
    {
        "prompt": (
            "The Pioneer 10 and 11 spacecraft were the first vehicles of humankind "
            "to venture beyond the limits of ours solar system."
        ),
        "options": {"A": "were the first", "B": "of humankind", "C": "to venture beyond", "D": "ours solar system"},
        "correct_answer": "D",
        "explanation": "Se necesita el adjetivo posesivo 'our', no el pronombre posesivo 'ours'.",
    },
]


def seed() -> None:
    with Session(engine) as session:
        inserted = 0
        for item in STRUCTURE_QUESTIONS:
            session.add(
                Question(
                    section=Section.structure,
                    question_type=QuestionType.sentence_completion,
                    prompt=item["prompt"],
                    options=item["options"],
                    correct_answer=item["correct_answer"],
                    verified=False,
                    source=SOURCE,
                )
            )
            inserted += 1

        for item in WRITTEN_EXPRESSION_QUESTIONS:
            session.add(
                Question(
                    section=Section.written_expression,
                    question_type=QuestionType.error_identification,
                    prompt=item["prompt"],
                    options=item["options"],
                    correct_answer=item["correct_answer"],
                    verified=False,
                    explanation=item.get("explanation"),
                    source=SOURCE,
                )
            )
            inserted += 1

        session.commit()
        print(
            f"{inserted} preguntas insertadas ({len(STRUCTURE_QUESTIONS)} structure + "
            f"{len(WRITTEN_EXPRESSION_QUESTIONS)} written expression). Sin skills."
        )


if __name__ == "__main__":
    seed()
