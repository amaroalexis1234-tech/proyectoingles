"""
Carga las preguntas de Reading Comprehension del "Exam 2" (TOEFL POST-TEST)
extraidas de TOEFL_tests_2026.pdf (paginas 452-460): 5 passages, 50 preguntas.

Mismas advertencias que los seeds anteriores: verified=False (respuestas
por comprension de lectura, no de un answer key oficial). Este post-test
tampoco trae tabla de skills en el material extraido -> sin skills.

Uso:
    python -m scripts.seed_exam2_reading
"""
from sqlmodel import Session

from app.core.database import engine
from app.modules.question_bank.models import Passage, Question, QuestionType, Section

SOURCE = "TOEFL_tests_2026.pdf - Exam 2 Reading Comprehension / POST-TEST (p.452-460)"

PASSAGES = [
    {
        "title": "Solar Eclipses",
        "text": (
            "A solar eclipse occurs when the Moon moves in front of the Sun and hides "
            "at least some part of the Sun from the earth. In a partial eclipse, the "
            "Moon covers part of the Sun; in an annular eclipse, the Moon covers the "
            "center of the Sun, leaving a bright ring of light around the Moon; in a "
            "total eclipse, the Sun is completely covered by the Moon.\n\n"
            "It seems rather improbable that a celestial body the size of the Moon "
            "could completely block out the tremendously immense Sun, as happens "
            "during a total eclipse, but this is exactly what happens. Although the "
            "Moon is considerably smaller in size than the Sun, the Moon is able to "
            "cover the Sun because of their relative distances from Earth. A total "
            "eclipse can last up to 7 minutes, during which time the Moon's shadow "
            "moves across Earth at a rate of about .6 kilometers per second."
        ),
        "questions": [
            {
                "prompt": "This passage mainly",
                "options": {
                    "A": "describes how long an eclipse will last",
                    "B": "gives facts about the Moon",
                    "C": "explains how the Sun is able to obscure the Moon",
                    "D": "informs the reader about solar eclipses",
                },
                "correct_answer": "D",
            },
            {
                "prompt": "In which type of eclipse is the Sun obscured in its entirety?",
                "options": {
                    "A": "A partial eclipse",
                    "B": "An annular eclipse",
                    "C": "A total eclipse",
                    "D": "A celestial eclipse",
                },
                "correct_answer": "C",
            },
            {
                "prompt": 'The word "ring" in line 3 could best be replaced by',
                "options": {"A": "piece of gold", "B": "circle", "C": "jewel", "D": "bell"},
                "correct_answer": "B",
            },
            {
                "prompt": 'A "celestial body" in line 5 is most probably one that is found',
                "options": {
                    "A": "within the Moon's shadow",
                    "B": "somewhere in the sky",
                    "C": "on the surface of the Sun",
                    "D": "inside Earth's atmosphere",
                },
                "correct_answer": "B",
            },
            {
                "prompt": 'What is the meaning of "block out" in line 5?',
                "options": {"A": "Square", "B": "Cover", "C": "Evaporate", "D": "Shrink"},
                "correct_answer": "B",
            },
            {
                "prompt": "According to the passage, how can the Moon hide the Sun during a total eclipse?",
                "options": {
                    "A": "The fact that the Moon is closer to Earth than the Sun makes up for the Moon's smaller size.",
                    "B": "The Moon can only obscure the Sun because of the Moon's great distance from the earth.",
                    "C": "Because the Sun is relatively close to Earth, the Sun can be eclipsed by the Moon.",
                    "D": "The Moon hides the Sun because of the Moon's considerable size.",
                },
                "correct_answer": "A",
            },
            {
                "prompt": 'The word "relative" in line 8 could best be replaced by',
                "options": {"A": "familial", "B": "infinite", "C": "comparative", "D": "paternal"},
                "correct_answer": "C",
            },
            {
                "prompt": "The passage states that which of the following happens during an eclipse?",
                "options": {
                    "A": "The Moon hides from the Sun.",
                    "B": "The Moon is obscured by the Sun.",
                    "C": "The Moon begins moving at a speed of .6 kilometers per second.",
                    "D": "The Moon's shadow crosses Earth.",
                },
                "correct_answer": "D",
            },
            {
                "prompt": 'The word "rate" in line 9 is closest in meaning to',
                "options": {"A": "form", "B": "speed", "C": "distance", "D": "rotation"},
                "correct_answer": "B",
            },
            {
                "prompt": "Where in the passage does the author mention the rate of a total eclipse?",
                "options": {"A": "Lines 1-2", "B": "Lines 2-4", "C": "Lines 5-6", "D": "Lines 8-9"},
                "correct_answer": "D",
            },
        ],
    },
    {
        "title": "Uncle Sam",
        "text": (
            "While the bald eagle is one national symbol of the United States, it is "
            "not the only one. Uncle Sam, a bearded gentleman costumed in the red, "
            "white, and blue stars and stripes of the nation's flag, is another "
            "well-known national symbol. According to legend, this character is based "
            "on Samuel Wilson, the owner of a meat-packing business in Troy, New York. "
            "During the War of 1812, Sam Wilson's company was granted a government "
            "contract to supply meat to the nation's soldiers; this meat was supplied "
            "to the army in barrels stamped with the initials U.S., which stood for "
            "United States. However, the country was at that time relatively young, "
            "and the initials U.S. were not commonly used. Many people questioned what "
            "the initials represented, and the standard reply became \"Uncle Sam,\" for "
            "the owner of the barrels. It is now generally accepted that the figure of "
            "Uncle Sam is based on Samuel Wilson, and the U.S. Congress has made it "
            "official by adopting a resolution naming Samuel Wilson as the inspiration "
            "for Uncle Sam."
        ),
        "questions": [
            {
                "prompt": "The paragraph preceding this passage most probably discusses",
                "options": {
                    "A": "the War of 1812",
                    "B": "the bald eagle, which symbolizes the United States",
                    "C": "Sam Wilson's meat-packing company",
                    "D": "the costume worn by Uncle Sam",
                },
                "correct_answer": "B",
            },
            {
                "prompt": "Which of the following is the most appropriate title for this passage?",
                "options": {
                    "A": "The Bald Eagle",
                    "B": "The Symbols of the United States",
                    "C": "Samuel Wilson",
                    "D": "Uncle Sam—Symbol of the Nation",
                },
                "correct_answer": "D",
            },
            {
                "prompt": "Which of the following is NOT mentioned about Uncle Sam's appearance?",
                "options": {
                    "A": "He wears facial hair.",
                    "B": "There is some blue in his clothing.",
                    "C": "He is bald.",
                    "D": "His clothes have stripes in them.",
                },
                "correct_answer": "C",
            },
            {
                "prompt": 'The word "costumed" in line 2 could most easily be replaced by',
                "options": {"A": "dressed", "B": "nationalized", "C": "hidden", "D": "seen"},
                "correct_answer": "A",
            },
            {
                "prompt": "Sam Wilson was the proprietor of what type of business?",
                "options": {
                    "A": "A costume company",
                    "B": "A meat-packing company",
                    "C": "A military clothier",
                    "D": "A barrel-making company",
                },
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "granted" in line 5 means',
                "options": {"A": "refused", "B": "underbid for", "C": "told about", "D": "given"},
                "correct_answer": "D",
            },
            {
                "prompt": "According to the passage, what was in the barrels stamped U.S.?",
                "options": {
                    "A": "Sam Wilson",
                    "B": "Food for the army",
                    "C": "Weapons to be used in the war",
                    "D": "Company contracts",
                },
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "initials" in line 6 means',
                "options": {"A": "nicknames", "B": "family names", "C": "first letters of words", "D": "company names"},
                "correct_answer": "C",
            },
            {
                "prompt": 'The word "official" in line 10 is closest in meaning to',
                "options": {"A": "authorized", "B": "professional", "C": "dutiful", "D": "accidental"},
                "correct_answer": "A",
            },
            {
                "prompt": (
                    'In 1812, people most probably answered that the letters "U.S." '
                    "written on the barrels stood for \"Uncle Sam\" because"
                ),
                "options": {
                    "A": "Congress required it",
                    "B": "Samuel Wilson was their favorite uncle",
                    "C": "Sam Wilson preferred it",
                    "D": "they were not exactly sure what the letters meant",
                },
                "correct_answer": "D",
            },
        ],
    },
    {
        "title": "Desert Vegetation",
        "text": (
            "Most people think of deserts as dry, flat areas with little vegetation "
            "and little or no rainfall, but this is hardly true. Many deserts have "
            "varied geographical formations ranging from soft, rolling hills to stark, "
            "jagged cliffs, and most deserts have a permanent source of water. Although "
            "deserts do not receive a high amount of rainfall—to be classified as a "
            "desert, an area must get less than twenty-five centimeters of rainfall "
            "per year—there are many plants that thrive on only small amounts of "
            "water, and deserts are often full of such plant life.\n\n"
            "Desert plants have a variety of mechanisms for obtaining the water needed "
            "for survival. Some plants, such as cactus, are able to store large "
            "amounts of water in their leaves or stems; after a rainfall these plants "
            "absorb a large supply of water to last until the next rainfall. Other "
            "plants, such as the mesquite, have extraordinarily deep root systems "
            "that allow them to obtain water from far below the desert's arid surface."
        ),
        "questions": [
            {
                "prompt": "What is the main topic of the passage?",
                "options": {
                    "A": "Deserts are dry, flat areas with few plants.",
                    "B": "There is little rainfall in the desert.",
                    "C": "Many kinds of vegetation can survive with little water.",
                    "D": "Deserts are not really flat areas with little plant life.",
                },
                "correct_answer": "C",
            },
            {
                "prompt": "The passage implies that",
                "options": {
                    "A": "the typical conception of a desert is incorrect",
                    "B": "all deserts are dry, flat areas",
                    "C": "most people are well informed about deserts",
                    "D": "the lack of rainfall in deserts causes the lack of vegetation",
                },
                "correct_answer": "A",
            },
            {
                "prompt": "The passage describes the geography of deserts as",
                "options": {"A": "flat", "B": "sandy", "C": "varied", "D": "void of vegetation"},
                "correct_answer": "C",
            },
            {
                "prompt": 'The word "source" in line 3 means',
                "options": {"A": "supply", "B": "storage space", "C": "need", "D": "lack"},
                "correct_answer": "A",
            },
            {
                "prompt": "According to the passage, what causes an area to be classified as a desert?",
                "options": {
                    "A": "The type of plants",
                    "B": "The geographical formations",
                    "C": "The amount of precipitation",
                    "D": "The source of water",
                },
                "correct_answer": "C",
            },
            {
                "prompt": 'The word "thrive" in line 5 means',
                "options": {"A": "suffer", "B": "grow well", "C": "minimally survive", "D": "decay"},
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "mechanisms" in line 7 could most easily be replaced by',
                "options": {"A": "machines", "B": "pumps", "C": "sources", "D": "methods"},
                "correct_answer": "D",
            },
            {
                "prompt": "Which of the following is mentioned in the passage about cacti?",
                "options": {
                    "A": "They have deep root systems.",
                    "B": "They retain water from one rainfall to the next.",
                    "C": "They survive in the desert because they do not need water.",
                    "D": "They get water from deep below the surface of the desert.",
                },
                "correct_answer": "B",
            },
            {
                "prompt": '"Mesquite" in line 10 is probably',
                "options": {"A": "a type of tree", "B": "a desert animal", "C": "a type of cactus", "D": "a geographical formation in the desert"},
                "correct_answer": "A",
            },
            {
                "prompt": 'The word "arid" in line 11 means',
                "options": {"A": "deep", "B": "dry", "C": "sandy", "D": "superficial"},
                "correct_answer": "B",
            },
            {
                "prompt": "Where in the passage does the author describe desert vegetation that keeps water in its leaves?",
                "options": {"A": "Lines 1-2", "B": "Lines 3-6", "C": "Lines 7-9", "D": "Lines 9-11"},
                "correct_answer": "C",
            },
        ],
    },
    {
        "title": "Scott Joplin and Ragtime",
        "text": (
            "American jazz is a conglomeration of sounds borrowed from such varied "
            "sources as American and African folk music, European classical music, "
            "and Christian gospel songs. One of the recognizable characteristics of "
            "jazz is its use of improvisation: certain parts of the music are written "
            "out and played the same way by various performers, and other improvised "
            "parts are created spontaneously during a performance and vary widely from "
            "performer to performer.\n\n"
            "The earliest form of jazz was ragtime, lively songs or rags performed on "
            "the piano, and the best-known of the ragtime performers and composers was "
            "Scott Joplin. Born in 1868 to former slaves, Scott Joplin earned his "
            "living from a very early age playing the piano in bars along the "
            "Mississippi. One of his regular jobs was in the Maple Leaf Club in "
            "Sedalia, Missouri. It was there that he began writing the more than 500 "
            'compositions that he was to produce, the most famous of which was "The '
            'Maple Leaf Rag."'
        ),
        "questions": [
            {
                "prompt": "This passage is about",
                "options": {
                    "A": "jazz in general and one specific type of jazz",
                    "B": "the various sources of jazz",
                    "C": "the life of Scott Joplin",
                    "D": "the major characteristics of jazz",
                },
                "correct_answer": "A",
            },
            {
                "prompt": 'The word "conglomeration" in line 1 could best be replaced by',
                "options": {"A": "disharmony", "B": "mixture", "C": "purity", "D": "treasure"},
                "correct_answer": "B",
            },
            {
                "prompt": 'In line 3, the word "improvisation" involves which of the following?',
                "options": {
                    "A": "Playing the written parts of the music",
                    "B": "Performing similarly to other musicians",
                    "C": "Making up music while playing",
                    "D": "Playing a varied selection of musical compositions",
                },
                "correct_answer": "C",
            },
            {
                "prompt": "According to the passage, ragtime was",
                "options": {
                    "A": "generally performed on a variety of instruments",
                    "B": "the first type of jazz",
                    "C": "extremely soothing and sedate",
                    "D": "performed only at the Maple Leaf Club in Sedalia",
                },
                "correct_answer": "B",
            },
            {
                "prompt": "Which of the following statements is true according to the passage?",
                "options": {
                    "A": "Scott Joplin was a slave when he was born.",
                    "B": "Scott Joplin's parents had been slaves before Scott was born.",
                    "C": "Scott Joplin had formerly been a slave, but he no longer was after 1868.",
                    "D": "Scott Joplin's parents were slaves when Scott was born.",
                },
                "correct_answer": "D",
            },
            {
                "prompt": 'The word "living" in line 8 could most easily be replaced by',
                "options": {"A": "money", "B": "life-style", "C": "enjoyment", "D": "health"},
                "correct_answer": "A",
            },
            {
                "prompt": 'The word "regular" in line 9 could best be replaced by',
                "options": {"A": "popular", "B": "steady", "C": "unusual", "D": "boring"},
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "which" in line 10 refers to',
                "options": {"A": "regular jobs", "B": "the Maple Leaf Club", "C": "Sedalia, Missouri", "D": "500 compositions"},
                "correct_answer": "D",
            },
            {
                "prompt": "The name of Scott Joplin's most famous composition probably came from",
                "options": {
                    "A": "the name of a saloon where he performed",
                    "B": "the maple tree near his Sedalia home",
                    "C": "the name of the town where he was born",
                    "D": "the school where he learned to play the piano",
                },
                "correct_answer": "A",
            },
            {
                "prompt": "The paragraph following the passage probably discusses",
                "options": {
                    "A": "Sedalia, Missouri",
                    "B": "the Maple Leaf Club",
                    "C": "the numerous compositions of Scott Joplin",
                    "D": "the life of Scott Joplin",
                },
                "correct_answer": "C",
            },
        ],
    },
    {
        "title": "Determinism",
        "text": (
            "The idea of determinism, that no event occurs in nature without natural "
            "causes, has been postulated as a natural law yet is under attack on both "
            "scientific and philosophical grounds. Scientific laws assume that a "
            "specific set of conditions will unerringly lead to a predetermined "
            "outcome. However, studies in the field of physics have demonstrated that "
            "the location and speed of minuscule particles such as electrons are the "
            "result of random behaviors rather than predictable results determined by "
            "pre-existing conditions. As a result of these studies, the principle of "
            "indeterminacy was formulated in 1925 by Werner Heisenberg. According to "
            "this principle, only the probable behavior of an electron can be "
            "predicted. The inability to absolutely predict the behavior of electrons "
            "casts doubt on the universal applicability of a natural law of "
            "determinism. Philosophically, the principal opposition to determinism "
            "emanates from those who see humans as creatures in possession of free "
            "will. Human decisions may be influenced by previous events, but the "
            "ultimate freedom of humanity may possibly lead to unforeseen choices, "
            "those not preordained by preceding events."
        ),
        "questions": [
            {
                "prompt": "It is implied in the passage that a natural law",
                "options": {
                    "A": "is something that applies to science only",
                    "B": "can be incontrovertibly found in the idea of determinism",
                    "C": "is philosophically unacceptable",
                    "D": "is a principle to which there is no exception",
                },
                "correct_answer": "D",
            },
            {
                "prompt": 'The word "unerringly" in line 3 could be most easily replaced by',
                "options": {"A": "fortunately", "B": "effortlessly", "C": "without mistake", "D": "with guidance"},
                "correct_answer": "C",
            },
            {
                "prompt": "The idea of determinism is refuted in this passage based on",
                "options": {
                    "A": "scientific proof",
                    "B": "data from the science and philosophy of determinism",
                    "C": "principles or assumptions from different fields of study",
                    "D": "philosophical doubt about free will",
                },
                "correct_answer": "C",
            },
            {
                "prompt": 'The word "minuscule" in line 4 is closest in meaning to',
                "options": {"A": "charged", "B": "fast-moving", "C": "circular", "D": "tiny"},
                "correct_answer": "D",
            },
            {
                "prompt": "According to the passage, which of the following is NOT true about the principle of indeterminacy?",
                "options": {
                    "A": "It was formulated based on studies in physics.",
                    "B": "It is philosophically unacceptable.",
                    "C": "It has been in existence for more than a decade.",
                    "D": "It is concerned with the random behavior of electrons.",
                },
                "correct_answer": "B",
            },
            {
                "prompt": 'The expression "emanates from" in line 10 could most easily be replaced by',
                "options": {"A": "derives from", "B": "differs from", "C": "is in contrast to", "D": "is subordinate to"},
                "correct_answer": "A",
            },
            {
                "prompt": "It is implied in the passage that free will is",
                "options": {
                    "A": "accepted by all philosophers",
                    "B": "a direct outcome of Werner's principle of indeterminacy",
                    "C": "the antithesis of determinism",
                    "D": "a natural law",
                },
                "correct_answer": "C",
            },
            {
                "prompt": 'The word "unforeseen" in line 12 is closest in meaning to',
                "options": {"A": "forewarned", "B": "blind", "C": "unappreciated", "D": "unpredictable"},
                "correct_answer": "D",
            },
            {
                "prompt": "Where in the passage does the author mention who developed the contrary principle to determinism?",
                "options": {"A": "Lines 1-2", "B": "Lines 6-7", "C": "Lines 8-9", "D": "Lines 9-13"},
                "correct_answer": "C",
            },
        ],
    },
]


def seed() -> None:
    with Session(engine) as session:
        inserted = 0
        for passage_data in PASSAGES:
            passage = Passage(title=passage_data["title"], text=passage_data["text"], source=SOURCE)
            session.add(passage)
            session.commit()
            session.refresh(passage)

            for item in passage_data["questions"]:
                session.add(
                    Question(
                        section=Section.reading,
                        question_type=QuestionType.multiple_choice,
                        prompt=item["prompt"],
                        options=item["options"],
                        correct_answer=item["correct_answer"],
                        verified=False,
                        passage_id=passage.id,
                        source=SOURCE,
                    )
                )
                inserted += 1

        session.commit()
        print(f"{inserted} preguntas de Reading (Exam 2) insertadas en {len(PASSAGES)} passages. Sin skills.")


if __name__ == "__main__":
    seed()
