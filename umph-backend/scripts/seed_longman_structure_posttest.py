"""
Carga las preguntas de Structure y Written Expression del POST-TEST
extraidas de LONGMAN_INTRODUCTORY_COURSE_PART2_PART3.pdf (paginas 133-138).

Mismas advertencias que los seeds anteriores: verified=False, sin skills.

Uso:
    python -m scripts.seed_longman_structure_posttest
"""
from sqlmodel import Session

from app.core.database import engine
from app.modules.question_bank.models import Question, QuestionType, Section

SOURCE = "LONGMAN_INTRODUCTORY_COURSE_PART2_PART3.pdf - Structure and Written Expression Post-Test (p.133-138)"

STRUCTURE_QUESTIONS = [
    {
        "prompt": "___ lived on Earth for nearly 150 million years.",
        "options": {"A": "Dinosaurs", "B": "Dinosaurs who", "C": "If dinosaurs", "D": "Since dinosaurs"},
        "correct_answer": "A",
    },
    {
        "prompt": "Early printers arranged type into ___ a small, flat composing stick.",
        "options": {"A": "words", "B": "are words on", "C": "words on", "D": "the words are on"},
        "correct_answer": "C",
    },
    {
        "prompt": "___ along most of its length into an upper chamber and a lower chamber.",
        "options": {
            "A": "The divided cochlea",
            "B": "Dividing the cochlea",
            "C": "The cochlea is divided",
            "D": "With a divided cochlea",
        },
        "correct_answer": "C",
    },
    {
        "prompt": "Yeast is an organic catalyst ___ known to prehistoric humanity.",
        "options": {"A": "was", "B": "which was", "C": "which it", "D": "which"},
        "correct_answer": "B",
    },
    {
        "prompt": "Many communities ___ a complex system of linguistic levels in order to show respect.",
        "options": {"A": "useful", "B": "use already made", "C": "making it useful", "D": "make use of"},
        "correct_answer": "D",
    },
    {
        "prompt": (
            "The ear is a flexible organ, ___ simply not designed to withstand the "
            "noise of modern living."
        ),
        "options": {"A": "but it", "B": "it", "C": "but", "D": "its"},
        "correct_answer": "A",
    },
    {
        "prompt": "In 1934, chemist Wallace Carothers produced a plastic which ___ nylon.",
        "options": {"A": "his call", "B": "he called", "C": "to call him", "D": "calling"},
        "correct_answer": "B",
    },
    {
        "prompt": "As ___ grows, the shell in which it lives grows, too.",
        "options": {"A": "a mollusk", "B": "a mollusk it", "C": "has a mollusk", "D": "it has a mollusk"},
        "correct_answer": "A",
    },
    {
        "prompt": "The first ___ the Civil War was fired from Fort Johnson upon Fort Sumter on April 12, 1861.",
        "options": {"A": "shot", "B": "shot in", "C": "shot was in", "D": "it was shot"},
        "correct_answer": "B",
    },
    {
        "prompt": "Stalactites are formed in caves by groundwater ___ dissolved lime.",
        "options": {"A": "it contains", "B": "containing", "C": "contains", "D": "containment"},
        "correct_answer": "B",
    },
    {
        "prompt": "By studying the movements of the Sun and Moon, even early astronomers could ___ eclipses would take place.",
        "options": {"A": "predicting when", "B": "when it predicts", "C": "the prediction when", "D": "predict when"},
        "correct_answer": "D",
    },
    {
        "prompt": "Coffee probably originally grew wild in Ethiopia in the province of Kaffe, and from there ___ to southern Arabia.",
        "options": {"A": "bringing it", "B": "it was brought", "C": "brought it", "D": "brought with it"},
        "correct_answer": "B",
    },
    {
        "prompt": "Alabama was occupied by the French and Spanish before ___ to England in 1763.",
        "options": {"A": "was ceded", "B": "ceded to it", "C": "it was ceded", "D": "ceded it"},
        "correct_answer": "C",
    },
    {
        "prompt": "A group of winged reptiles ___ pterosaurs is believed to have been the first vertebrates with the power of flight.",
        "options": {"A": "call", "B": "calls", "C": "called", "D": "is called"},
        "correct_answer": "C",
    },
    {
        "prompt": (
            "On November 23, 1863, Grant stunned the Confederates on Missionary "
            "Ridge with what ___ to be a full-dress military parade of troops who "
            "unexpectedly opened fire."
        ),
        "options": {"A": "appeared", "B": "appearing", "C": "appearance", "D": "apparent"},
        "correct_answer": "A",
    },
]

WRITTEN_EXPRESSION_QUESTIONS = [
    {
        "prompt": "Vast flows of information is carried on hair-thin fiber-optic cables.",
        "options": {"A": "Vast flows", "B": "of information", "C": "is carried", "D": "hair-thin"},
        "correct_answer": "C",
        "explanation": "El sujeto 'flows' es plural: el verbo debe ser 'are carried', no 'is carried'.",
    },
    {
        "prompt": "The crafting of fine violins has been proceeding for several century as a secret art.",
        "options": {"A": "The crafting", "B": "has been proceeding", "C": "for several century", "D": "as a secret art"},
        "correct_answer": "C",
        "explanation": "Con 'several' se necesita el plural: 'several centuries', no 'several century'.",
    },
    {
        "prompt": "Linguistic conflicts due to divided ethnic and national loyalties can be both bitter or violent.",
        "options": {"A": "Linguistic conflicts", "B": "due to divided", "C": "can be both", "D": "or violent"},
        "correct_answer": "D",
        "explanation": "La pareja correcta es 'both...and', no 'both...or': debe ser 'and violent'.",
    },
    {
        "prompt": "In 1851, with the publication of hers antislavery novel, Harriet Beecher Stowe rocketed to fame.",
        "options": {"A": "with the publication of", "B": "hers antislavery", "C": "rocketed to", "D": "fame"},
        "correct_answer": "B",
        "explanation": "Se necesita el adjetivo posesivo 'her', no el pronombre posesivo 'hers'.",
    },
    {
        "prompt": "The smallest and simple living organisms on Earth are bacteria.",
        "options": {"A": "The smallest and", "B": "simple", "C": "living organisms", "D": "are bacteria"},
        "correct_answer": "B",
        "explanation": "Estructura paralela con 'smallest': debe ser el superlativo 'simplest', no 'simple'.",
    },
    {
        "prompt": "The effort to determine the exact numerical value of pi has now reach 2.16 billion decimal digits.",
        "options": {"A": "The effort to determine", "B": "numerical value", "C": "has now reach", "D": "decimal digits"},
        "correct_answer": "C",
        "explanation": "Presente perfecto: debe ser 'has now reached', no 'has now reach'.",
    },
    {
        "prompt": "The hammerhead shark is usual found in warm, temperate waters.",
        "options": {"A": "The hammerhead shark", "B": "is usual found", "C": "warm, temperate", "D": "waters"},
        "correct_answer": "B",
        "explanation": "Se necesita el adverbio 'usually' para modificar 'found', no el adjetivo 'usual'.",
    },
    {
        "prompt": "Princeton University, which was establish in 1746, is one of the oldest universities in the United States.",
        "options": {"A": "which was establish", "B": "in 1746", "C": "is one of", "D": "oldest universities"},
        "correct_answer": "A",
        "explanation": "Voz pasiva: debe ser 'was established', no 'was establish'.",
    },
    {
        "prompt": "According to a World Resources Institute report, a significant part of forest acreage disappear each year.",
        "options": {"A": "According to", "B": "a significant part", "C": "disappear", "D": "each year"},
        "correct_answer": "C",
        "explanation": "El sujeto 'a significant part' es singular: el verbo debe ser 'disappears', no 'disappear'.",
    },
    {
        "prompt": "The Earth's crust is composed of 15 plates which float on the partially molten layer below they.",
        "options": {"A": "is composed", "B": "which float", "C": "partially molten", "D": "below they"},
        "correct_answer": "D",
        "explanation": "Después de la preposición 'below' se necesita el pronombre objeto 'them', no 'they'.",
    },
    {
        "prompt": "As one climbs high up a mountain, the air becomes both colder or thinner.",
        "options": {"A": "As one climbs", "B": "high up", "C": "becomes both", "D": "colder or thinner"},
        "correct_answer": "D",
        "explanation": "La pareja correcta es 'both...and': debe ser 'colder and thinner', no 'colder or thinner'.",
    },
    {
        "prompt": "When a bone is broke into several pieces, doctors may pin the pieces together for proper healing.",
        "options": {"A": "is broke", "B": "into several pieces", "C": "may pin", "D": "for proper healing"},
        "correct_answer": "A",
        "explanation": "Voz pasiva: debe ser 'is broken', no 'is broke'.",
    },
    {
        "prompt": "The long necks of much plant-eating dinosaurs were useful for reaching up to the treetops to feed.",
        "options": {"A": "The long necks of", "B": "much plant-eating", "C": "were useful", "D": "to feed"},
        "correct_answer": "B",
        "explanation": "'Dinosaurs' es contable en plural: se usa 'many', no 'much'.",
    },
    {
        "prompt": "Hippocrates believed that good health was dependently on the balance of the four fluids of the body.",
        "options": {"A": "believed", "B": "was dependently on", "C": "the balance of", "D": "of the body"},
        "correct_answer": "B",
        "explanation": "Se necesita el adjetivo 'dependent', no el adverbio 'dependently': 'was dependent on'.",
    },
    {
        "prompt": "A jet stream is a flat and narrow tube of air that moves more rapid than the surrounding air.",
        "options": {"A": "a flat and narrow", "B": "that moves more rapid", "C": "than the surrounding", "D": "air"},
        "correct_answer": "B",
        "explanation": "Se necesita el adverbio 'rapidly' para modificar 'moves', no el adjetivo 'rapid'.",
    },
    {
        "prompt": (
            "Because mistletoe berries are poisonous, everyone with Christmas "
            "decorations containing mistletoe need to be aware of the potential danger."
        ),
        "options": {"A": "are poisonous", "B": "containing", "C": "need to be aware", "D": "potential danger"},
        "correct_answer": "C",
        "explanation": "El sujeto 'everyone' es singular: el verbo debe ser 'needs', no 'need'.",
    },
    {
        "prompt": (
            "When Pierre L'Enfant designed the national capital in 1791, her envisioned "
            "a broad boulevard linking the White House and the Capitol."
        ),
        "options": {"A": "designed", "B": "in 1791", "C": "her envisioned", "D": "linking"},
        "correct_answer": "C",
        "explanation": "Pierre L'Enfant es hombre: el pronombre debe ser 'he', no 'her'.",
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
            "Cavemen created a large amount of early works of art using a mixture "
            "of clay, chalk, and burned wood and bones."
        ),
        "options": {"A": "a large amount of", "B": "a mixture of", "C": "burned", "D": "bones"},
        "correct_answer": "A",
        "explanation": "'Works of art' es contable en plural: se usa 'a large number of', no 'a large amount of'.",
    },
    {
        "prompt": (
            "Variations in melody, rhythm, and tone of voice becomes a major feature "
            "of child speech toward the end of the first year."
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
            f"{len(WRITTEN_EXPRESSION_QUESTIONS)} written expression). Sin skills."
        )


if __name__ == "__main__":
    seed()
