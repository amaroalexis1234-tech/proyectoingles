"""
Carga las preguntas de Structure y Written Expression del "Exam 2"
extraidas de TOEFL_tests_2026.pdf (paginas 331-337).

Mismas advertencias que scripts/seed_exam1_structure.py sobre
verified=False (respuestas determinadas por analisis gramatical).

ADICIONAL para Exam 2: el material extraido de este post-test NO incluye
la tabla "pregunta -> skill" que si trae el pre-test del Exam 1. Por eso
estas preguntas se cargan SIN skills asociados (lista vacia). Si se
consigue esa tabla despues, se pueden vincular sin tocar las preguntas.

Uso:
    python -m scripts.seed_exam2_structure
"""
from sqlmodel import Session

from app.core.database import engine
from app.modules.question_bank.models import Question, QuestionType, Section

SOURCE = "TOEFL_tests_2026.pdf - Exam 2 Structure and Written Expression (p.331-337)"

STRUCTURE_QUESTIONS = [
    {
        "prompt": "___ range in color from pale yellow to bright orange.",
        "options": {"A": "Canaries", "B": "Canaries which", "C": "That canaries", "D": "Canaries that are"},
        "correct_answer": "A",
    },
    {
        "prompt": "Carnivorous plants ___ insects to obtain nitrogen.",
        "options": {
            "A": "are generally trapped",
            "B": "trap generally",
            "C": "are trapped generally",
            "D": "generally trap",
        },
        "correct_answer": "D",
    },
    {
        "prompt": "A federal type of government results in ___.",
        "options": {
            "A": "a vertical distribution of power",
            "B": "power is distributed vertically",
            "C": "vertically distributed",
            "D": "the distribution of power is vertical",
        },
        "correct_answer": "A",
    },
    {
        "prompt": "February normally has twenty-eight days, but every fourth year, ___ has twenty-nine.",
        "options": {"A": "there", "B": "its", "C": "is a leap year", "D": "a leap year, it"},
        "correct_answer": "D",
    },
    {
        "prompt": "Evidence suggests that one-quarter of operations ___ bypass surgery may be unnecessary.",
        "options": {"A": "they involve", "B": "involve", "C": "involving", "D": "which they involve"},
        "correct_answer": "C",
    },
    {
        "prompt": (
            "___ a tornado spins in a counterclockwise direction in the northern "
            "hemisphere, it spins in the opposite direction in the southern hemisphere."
        ),
        "options": {"A": "However", "B": "Because of", "C": "Although", "D": "That"},
        "correct_answer": "C",
    },
    {
        "prompt": "The Caldecott Medal, ___ for the best children's picture book, is awarded each January.",
        "options": {"A": "is a prize which", "B": "which prize", "C": "which is a prize", "D": "is a prize"},
        "correct_answer": "C",
    },
    {
        "prompt": (
            "Sports medicine is a medical specialty that deals with the identification "
            "and treatment of injuries to persons ___."
        ),
        "options": {
            "A": "sports are involved",
            "B": "involved in sports",
            "C": "they are involved in sports",
            "D": "sports involve them",
        },
        "correct_answer": "B",
    },
    {
        "prompt": (
            "The Wilmington Oil Field, in Long Beach, California, is one of ___ oil "
            "fields in the continental United States."
        ),
        "options": {"A": "productive", "B": "the most productive", "C": "most are productive", "D": "productivity"},
        "correct_answer": "B",
    },
    {
        "prompt": (
            "Thunder occurs as ___ through air, causing the heated air to expand and "
            "collide with layers of cooler air."
        ),
        "options": {
            "A": "an electrical charge",
            "B": "passes an electrical charge",
            "C": "the passing of an electrical charge",
            "D": "an electrical charge passes",
        },
        "correct_answer": "D",
    },
    {
        "prompt": "The population of Houston was ravaged by yellow fever in 1839 ___ in 1867.",
        "options": {"A": "it happened again", "B": "and again", "C": "was ravaged again", "D": "again once more"},
        "correct_answer": "B",
    },
    {
        "prompt": (
            "Researchers have long debated ___ Saturn's moon Titan contains "
            "hydrocarbon oceans and lakes."
        ),
        "options": {"A": "over it", "B": "whether the", "C": "whether over", "D": "whether"},
        "correct_answer": "D",
    },
    {
        "prompt": "According to Bernoulli's principle, the higher the speed of a fluid gas, ___ the pressure.",
        "options": {"A": "it will be lower", "B": "lower than the", "C": "the lower", "D": "lower it is"},
        "correct_answer": "C",
    },
    {
        "prompt": (
            "The flight instructor, ___ at the air base, said that orders not to fight "
            "had been issued."
        ),
        "options": {"A": "when interviewed", "B": "when he interviewed", "C": "when to interview", "D": "when interviewing"},
        "correct_answer": "A",
    },
    {
        "prompt": "In the northern and central parts of the state of Idaho ___ and churning rivers.",
        "options": {
            "A": "majestic mountains are found",
            "B": "are majestic mountains found",
            "C": "are found majestic mountains",
            "D": "finding majestic mountains",
        },
        "correct_answer": "C",
    },
]

WRITTEN_EXPRESSION_QUESTIONS = [
    {
        "prompt": "Light can travels from the Sun to the Earth in eight minutes and twenty seconds.",
        "options": {"A": "Light", "B": "can travels", "C": "in eight minutes and", "D": "twenty seconds"},
        "correct_answer": "B",
        "explanation": "Después de un modal ('can') se usa la forma base del verbo: 'can travel', no 'can travels'.",
    },
    {
        "prompt": "Every human typically have twenty-three pairs of chromosomes in most cells.",
        "options": {"A": "Every human", "B": "typically have", "C": "pairs of", "D": "most cells"},
        "correct_answer": "B",
        "explanation": "'Every human' es singular; el verbo debe ser 'has', no 'have'.",
    },
    {
        "prompt": "In the sport of fencing, three type of swords are used: the foil, the epee, and the sabre.",
        "options": {"A": "In the sport of", "B": "three type", "C": "are used", "D": "the sabre"},
        "correct_answer": "B",
        "explanation": "Con 'three' se necesita el plural: 'three types', no 'three type'.",
    },
    {
        "prompt": (
            "The Internal Revenue Service uses computers to check tax return "
            "computations, to determine the reasonableness of deductions, and for "
            "verifying the accuracy of reported income."
        ),
        "options": {"A": "uses", "B": "computations", "C": "for verifying", "D": "reported income"},
        "correct_answer": "C",
        "explanation": "Estructura paralela con 'to check...to determine': debe ser 'to verify', no 'for verifying'.",
    },
    {
        "prompt": "There was four groups of twenty rats each involved in the test.",
        "options": {"A": "There was", "B": "of twenty rats", "C": "each involved", "D": "the test"},
        "correct_answer": "A",
        "explanation": "El sujeto real 'four groups' es plural: debe ser 'There were', no 'There was'.",
    },
    {
        "prompt": (
            'The type of jazz known as "swing" was introduced by Duke Ellington when '
            'he wrote and records "It Don\'t Mean a Thing If It Ain\'t Got That Swing."'
        ),
        "options": {"A": "known as", "B": "was introduced", "C": "wrote and", "D": "records"},
        "correct_answer": "D",
        "explanation": "Estructura paralela: 'wrote and recorded', no 'wrote and records'.",
    },
    {
        "prompt": "The bones of mammals, not alike those of other vertebrates, show a high degree of differentiation.",
        "options": {"A": "not alike", "B": "those of other", "C": "show", "D": "of differentiation"},
        "correct_answer": "A",
        "explanation": "La forma correcta de comparación negativa es 'unlike', no 'not alike'.",
    },
    {
        "prompt": "The United States receives a large amount of revenue from taxation of a tobacco products.",
        "options": {"A": "receives", "B": "a large amount", "C": "taxation of a", "D": "tobacco products"},
        "correct_answer": "C",
        "explanation": "El artículo 'a' no puede preceder a un sustantivo plural: 'tobacco products' no lleva 'a'.",
    },
    {
        "prompt": "Much fats are composed of one molecule of glycerin combined with three molecules of fatty acids.",
        "options": {"A": "Much fats", "B": "one molecule of", "C": "combined with", "D": "of fatty acids"},
        "correct_answer": "A",
        "explanation": "'Fats' es contable en plural: se usa 'Many fats', no 'Much fats'.",
    },
    {
        "prompt": "The capital of the Confederacy was originally in Mobile, but they were moved to Richmond.",
        "options": {"A": "The capital", "B": "originally", "C": "they were moved", "D": "to Richmond"},
        "correct_answer": "C",
        "explanation": "El pronombre debe concordar con 'capital' (singular): 'it was moved', no 'they were moved'.",
    },
    {
        "prompt": (
            "A pearl develops when a tiny grain of sand or some another irritant "
            "accidentally enters into the shell of a pearl oyster."
        ),
        "options": {"A": "when", "B": "some another", "C": "accidentally", "D": "enters into"},
        "correct_answer": "B",
        "explanation": "Redundante: debe ser simplemente 'another' o 'some other', no 'some another'.",
    },
    {
        "prompt": "The English horn is an alto oboe with a pitch one fifth lower as that of the soprano oboe.",
        "options": {"A": "an alto oboe", "B": "a pitch", "C": "as that of", "D": "the soprano oboe"},
        "correct_answer": "C",
        "explanation": "El comparativo correcto es 'lower than', no 'lower as'.",
    },
    {
        "prompt": "In the Milky Way galaxy, the most recent observed supernova appeared in 1604.",
        "options": {"A": "the most recent", "B": "observed", "C": "appeared", "D": "in 1604"},
        "correct_answer": "A",
        "explanation": "Se necesita el adverbio 'recently' para modificar 'observed', no el adjetivo 'recent'.",
    },
    {
        "prompt": (
            "Although the name suggests otherwise, the ship known as Old Ironsides was "
            "built of oak and cedar rather than it was built of iron."
        ),
        "options": {"A": "Although", "B": "otherwise", "C": "known as", "D": "it was built of"},
        "correct_answer": "D",
        "explanation": "Estructura paralela con 'of oak and cedar': debe ser 'rather than of iron', sin repetir la cláusula.",
    },
    {
        "prompt": "Never in the history of humanity there have been more people living on this relatively small planet.",
        "options": {"A": "Never in the history", "B": "there have been", "C": "living on", "D": "relatively small planet"},
        "correct_answer": "B",
        "explanation": "Con 'Never' al inicio se requiere inversión: 'have there been', no 'there have been'.",
    },
    {
        "prompt": "Because of the mobile of Americans today, it is difficult for them to put down real roots.",
        "options": {"A": "the mobile", "B": "it is difficult", "C": "for them", "D": "real roots"},
        "correct_answer": "A",
        "explanation": "Se necesita el sustantivo 'mobility', no el adjetivo 'mobile'.",
    },
    {
        "prompt": (
            "For five years after the Civil War, Robert E. Lee served to president of "
            "Washington College, which later was called Washington and Lee."
        ),
        "options": {"A": "For five years after", "B": "served to president", "C": "which later", "D": "was called"},
        "correct_answer": "B",
        "explanation": "La preposición correcta es 'served as president', no 'served to president'.",
    },
    {
        "prompt": "In a copperhead snake, the venom flows from a single venom glands to a pair of hollow teeth.",
        "options": {"A": "the venom flows", "B": "a single venom glands", "C": "to a pair of", "D": "hollow teeth"},
        "correct_answer": "B",
        "explanation": "'A single' requiere el sustantivo en singular: 'gland', no 'glands'.",
    },
    {
        "prompt": "A hawk swallows its food in large pieces, digests some of it, and regurgitating the rest.",
        "options": {"A": "swallows", "B": "digests some of it", "C": "and", "D": "regurgitating"},
        "correct_answer": "D",
        "explanation": "Estructura paralela: 'swallows...digests...and regurgitates', no 'regurgitating'.",
    },
    {
        "prompt": "Defects can occurring when liquid helium undergoes a phase transition to its superfluid phase.",
        "options": {"A": "Defects can occurring", "B": "undergoes", "C": "a phase transition", "D": "superfluid phase"},
        "correct_answer": "A",
        "explanation": "Después de un modal se usa la forma base: 'can occur', no 'can occurring'.",
    },
    {
        "prompt": (
            "Cavemen created a large amount of early works of art using a mixture of "
            "clay, chalk, and burned wood and bones."
        ),
        "options": {"A": "a large amount of", "B": "a mixture of", "C": "burned", "D": "bones"},
        "correct_answer": "A",
        "explanation": "'Works of art' es contable en plural: se usa 'a large number of', no 'a large amount of'.",
    },
    {
        "prompt": (
            "Variations in melody, rhythm, and tone of voice becomes a major feature of "
            "child speech toward the end of the first year."
        ),
        "options": {"A": "Variations in", "B": "becomes", "C": "a major feature", "D": "toward the end"},
        "correct_answer": "B",
        "explanation": "El sujeto plural 'Variations' exige 'become', no 'becomes'.",
    },
    {
        "prompt": "As a protective protein molecule, an antibody can combines with a foreign virus protein.",
        "options": {"A": "As a protective", "B": "can combines", "C": "with a foreign", "D": "virus protein"},
        "correct_answer": "B",
        "explanation": "Después de un modal se usa la forma base: 'can combine', no 'can combines'.",
    },
    {
        "prompt": "The water moccasin is a high venomous and extremely dangerous pit viper.",
        "options": {"A": "is a high venomous", "B": "and extremely", "C": "dangerous", "D": "pit viper"},
        "correct_answer": "A",
        "explanation": "Se necesita el adverbio 'highly' para modificar 'venomous', no el adjetivo 'high'.",
    },
    {
        "prompt": (
            "Though aluminum is more common than iron, it is extremely difficult to "
            "break their hold on other atoms."
        ),
        "options": {"A": "Though", "B": "more common than", "C": "break their hold", "D": "other atoms"},
        "correct_answer": "C",
        "explanation": "El pronombre debe concordar con 'aluminum' (singular): 'its hold', no 'their hold'.",
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
            f"{len(WRITTEN_EXPRESSION_QUESTIONS)} written expression). Sin skills (no disponibles en el post-test)."
        )


if __name__ == "__main__":
    seed()
