"""
Carga las preguntas de Reading Comprehension del PRE-TEST extraidas de
LONGMAN_INTRODUCTORY_COURSE_PART2_PART3.pdf (paginas 143-153): 5 passages,
50 preguntas. Mismas advertencias: verified=False, sin skills.

Uso:
    python -m scripts.seed_longman_reading_pretest
"""
from sqlmodel import Session

from app.core.database import engine
from app.modules.question_bank.models import Passage, Question, QuestionType, Section

SOURCE = "LONGMAN_INTRODUCTORY_COURSE_PART2_PART3.pdf - Reading Comprehension Pre-Test (p.143-153)"

PASSAGES = [
    {
        "title": "The Cullinan Diamond",
        "text": (
            "The largest diamond ever found is the Cullinan Diamond. This diamond "
            "weighed 3,106 carats in its uncut state when it was discovered in South "
            "Africa on January 25, 1905.\n\n"
            "The Cullinan Diamond was cut into 9 major stones and 96 smaller ones. "
            "The largest of the cut stones, and still the largest cut diamond in the "
            "world, is the pear-shaped Cullinan I at 530 carats. This diamond, which "
            "is also known as the Greater Star of Africa, is more than 2 inches "
            "(5.4 cm) long and 1.75 inches (4.4 cm) wide. It became part of the "
            "British crown jewels in 1907."
        ),
        "questions": [
            {
                "prompt": "What is the best title for this passage?",
                "options": {
                    "A": "Diamond Cutting",
                    "B": "The World's Biggest Diamond, Uncut and Cut",
                    "C": "Measuring Diamonds in Carats",
                    "D": "The British Crown Jewels",
                },
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "uncut" in line 2 is closest in meaning to which of the following?',
                "options": {"A": "Finished", "B": "Unnatural", "C": "Pear", "D": "Whole"},
                "correct_answer": "D",
            },
            {
                "prompt": 'The word "discovered" in line 2 is closest in meaning to',
                "options": {"A": "created", "B": "found", "C": "buried", "D": "weighed"},
                "correct_answer": "B",
            },
            {
                "prompt": "It can be inferred from the passage that the Cullinan Diamond was cut into how many total stones?",
                "options": {"A": "9", "B": "96", "C": "105", "D": "3,106"},
                "correct_answer": "C",
            },
            {
                "prompt": 'The word "major" in line 3 could best be replaced by',
                "options": {"A": "well-known", "B": "military", "C": "natural", "D": "big"},
                "correct_answer": "D",
            },
            {
                "prompt": "Which of the following is NOT true about Cullinan I?",
                "options": {
                    "A": "It was cut from the Cullinan Diamond.",
                    "B": "It weighs 3,106 carats.",
                    "C": "It is the biggest cut diamond in the world.",
                    "D": "It is sometimes called the Greater Star of Africa.",
                },
                "correct_answer": "B",
            },
            {
                "prompt": "All of the following are true about the shape of the Greater Star of Africa EXCEPT that",
                "options": {
                    "A": "it is in the shape of a pear",
                    "B": "it is 5.4 centimeters long",
                    "C": "it is longer than it is wide",
                    "D": "it is 4.4 inches wide",
                },
                "correct_answer": "D",
            },
            {
                "prompt": "According to the passage, what happened to Cullinan I?",
                "options": {
                    "A": "It remained in Africa.",
                    "B": "It was cut into smaller stones.",
                    "C": "It was cut and changed into the Greater Star of Africa.",
                    "D": "It became the property of the British Royal family.",
                },
                "correct_answer": "D",
            },
            {
                "prompt": "Where in the passage does the author mention the Cullinan Diamond's weight when it was mined?",
                "options": {"A": "Lines 1-2", "B": "Line 3", "C": "Lines 4-5", "D": "Line 6"},
                "correct_answer": "A",
            },
        ],
    },
    {
        "title": "Coca-Cola",
        "text": (
            "Coca-Cola was invented in 1886 by Atlanta pharmacist John S. "
            "Pemberton. The name for the product was actually proposed by "
            "Pemberton's assistant, Frank Robinson. The name was taken from the two "
            "most unusual ingredients in the drink, the South American coca leaf and "
            "the African cola nut.\n\n"
            "The recipe for today's Coca-Cola is very well guarded. Many of the "
            "ingredients are known; in addition to coca leaves and cola nut, they "
            "include lemon, orange, lime, cinnamon, nutmeg, vanilla, caramel, and "
            "sugar. The proportions of the ingredients and the identity of Coke's "
            "secret ingredients are known by only a few of the Coca-Cola Company's "
            "senior corporate officers."
        ),
        "questions": [
            {
                "prompt": "The passage mainly discusses",
                "options": {
                    "A": "the success of the Coca-Cola Company",
                    "B": "the unusual ingredients in Coca-Cola",
                    "C": "John S. Pemberton",
                    "D": "Coca-Cola's recipe and who developed it",
                },
                "correct_answer": "D",
            },
            {
                "prompt": "According to the passage, who created Coca-Cola?",
                "options": {
                    "A": "The Coca-Cola Company",
                    "B": "John S. Pemberton",
                    "C": "Pemberton's assistant",
                    "D": "Frank Robinson",
                },
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "unusual" in line 3 is closest in meaning to',
                "options": {"A": "uncommon", "B": "important", "C": "unused", "D": "tasty"},
                "correct_answer": "A",
            },
            {
                "prompt": "Which of the following is NOT true about the name Coca-Cola?",
                "options": {
                    "A": 'The name "coca" comes from the coca leaf.',
                    "B": 'The name "cola" comes from the cola nut.',
                    "C": "Frank Robinson suggested the name.",
                    "D": "The inventor came up with the name.",
                },
                "correct_answer": "D",
            },
            {
                "prompt": 'A "recipe" in line 5 is',
                "options": {
                    "A": "information about drugs for a pharmacy",
                    "B": "a description of how to prepare something",
                    "C": "an accounting statement",
                    "D": "a corporate organizational plan",
                },
                "correct_answer": "B",
            },
            {
                "prompt": "The passage states that the recipe for Coca-Cola is",
                "options": {
                    "A": "well known",
                    "B": "known by only a limited number of people",
                    "C": "unknown",
                    "D": "published information",
                },
                "correct_answer": "B",
            },
            {
                "prompt": "Which of the following is NOT mentioned as an ingredient of Coca-Cola?",
                "options": {"A": "Orange leaves", "B": "Nutmeg", "C": "Citrus fruits", "D": "Sugar"},
                "correct_answer": "A",
            },
            {
                "prompt": 'The word "secret" in line 7 could best be replaced by',
                "options": {"A": "unrevealed", "B": "delicious", "C": "business", "D": "speechless"},
                "correct_answer": "A",
            },
            {
                "prompt": "It can be inferred from the passage that",
                "options": {
                    "A": "the public knows all the ingredients in Coca-Cola",
                    "B": "the public is not sure that coca leaves are used in Coca-Cola",
                    "C": "the public does not know how many cola nuts are used in a batch of Coca-Cola",
                    "D": "no one knows the exact proportions of ingredients used in Coca-Cola",
                },
                "correct_answer": "D",
            },
            {
                "prompt": 'The word "senior" in line 8 could best be replaced by',
                "options": {"A": "trustworthy", "B": "high-level", "C": "more mature", "D": "really decisive"},
                "correct_answer": "B",
            },
            {
                "prompt": "Where in the passage does the author mention who gave Coca-Cola its name?",
                "options": {"A": "Lines 1-2", "B": "Lines 3-4", "C": "Line 5", "D": "Lines 7-8"},
                "correct_answer": "A",
            },
        ],
    },
    {
        "title": "Mount Everest and Mauna Kea",
        "text": (
            "Most people would say that the world's tallest mountain is Mount "
            "Everest. This mountain in the Himalayas is just over 29,000 feet high.\n\n"
            "However, if mountains are measured a little bit differently, then the "
            "tallest mountain on Earth is Mauna Kea, in the Hawaiian Islands. Mauna "
            "Kea is only about 14,000 feet above sea level, so in comparison to "
            "Mount Everest it just does not look anywhere near as high as Mount "
            "Everest to a person standing at sea level.\n\n"
            "Mauna Kea, however, does not begin at sea level. It rises from an "
            "ocean floor that is more than 16,000 feet below the surface of the "
            "water. This mountain therefore measures more than 30,000 feet from its "
            "base to its top, making it a higher mountain than Mount Everest."
        ),
        "questions": [
            {
                "prompt": "The main idea of the passage is that",
                "options": {
                    "A": "Mount Everest is the world's tallest mountain",
                    "B": "Mount Everest and Mauna Kea are located in different parts of the world",
                    "C": "Mauna Kea's base is below sea level",
                    "D": "Mauna Kea could be considered the tallest mountain in the world",
                },
                "correct_answer": "D",
            },
            {
                "prompt": "Which of the following is NOT stated about Mount Everest?",
                "options": {
                    "A": "Many people believe it is the world's tallest mountain.",
                    "B": "It is part of the Himalayas.",
                    "C": "It is over 29,000 feet high.",
                    "D": "It rises from the ocean floor.",
                },
                "correct_answer": "D",
            },
            {
                "prompt": 'The word "just" in line 2 could best be replaced by',
                "options": {"A": "noticeably", "B": "soon", "C": "barely", "D": "recently"},
                "correct_answer": "C",
            },
            {
                "prompt": 'The expression "a little bit" in line 3 is closest in meaning to',
                "options": {"A": "a small size", "B": "quite", "C": "somewhat", "D": "extremely"},
                "correct_answer": "C",
            },
            {
                "prompt": "According to the passage, Mauna Kea is how far above the level of the water?",
                "options": {"A": "14,000 feet", "B": "16,000 feet", "C": "29,000 feet", "D": "30,000 feet"},
                "correct_answer": "A",
            },
            {
                "prompt": 'The expression "in comparison to" in lines 4 and 5 could best be replaced by',
                "options": {"A": "close to", "B": "in relation to", "C": "as a result of", "D": "because of"},
                "correct_answer": "B",
            },
            {
                "prompt": "It is implied in the passage that Mauna Kea does not seem as tall as Mount Everest because",
                "options": {
                    "A": "people do not want to look at it",
                    "B": "part of Mauna Kea is under water",
                    "C": "Mount Everest has more snow",
                    "D": "Mauna Kea is in a different part of the world than Mount Everest",
                },
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "floor" in line 7 could best be replaced by',
                "options": {"A": "carpet", "B": "bottom", "C": "roof", "D": "water"},
                "correct_answer": "B",
            },
            {
                "prompt": "The passage indicates that Mauna Kea",
                "options": {
                    "A": "measures 16,000 feet from top to bottom",
                    "B": "is completely covered with water",
                    "C": "is more than half covered by water",
                    "D": "is 1,000 feet shorter than Mount Everest",
                },
                "correct_answer": "C",
            },
            {
                "prompt": "Where in the passage does the author mention Mount Everest's total height?",
                "options": {"A": "Lines 1-2", "B": "Lines 4-6", "C": "Line 7", "D": "Lines 8-9"},
                "correct_answer": "A",
            },
        ],
    },
    {
        "title": "The First Americans",
        "text": (
            "When Columbus arrived in the Americas in 1492, there were already an "
            "estimated thirty to forty million people living in North and South "
            "America. It has therefore been quite easy for some to refute the idea "
            'that Columbus "discovered" America. How and when these inhabitants '
            "came to America has been the source of much scientific research and "
            "discussion.\n\n"
            'Most archeologists agree that the first Americans, the true "discoverers" '
            "of America, came from northeastern Asia. There is also a considerable "
            "amount of proof that inhabitants have been in the Americas for at "
            "least 15,000 years.\n\n"
            "To get to the Americas, these people had to cross over the 55-mile-wide "
            "Bering Strait that separates Asia and North America. According to one "
            "theory, these people crossed over during periods when a land bridge "
            "existed between the two continents. During Ice Ages, so much of the "
            "Earth's water was frozen that the sea levels dropped, and it was "
            "possible to walk from Asia to North America."
        ),
        "questions": [
            {
                "prompt": "What is the author's main purpose?",
                "options": {
                    "A": "To explain how Columbus discovered America",
                    "B": "To show how people came to America before Columbus",
                    "C": "To demonstrate the importance to archeologists of northeastern Asia",
                    "D": "To explain how to cross the Bering Strait",
                },
                "correct_answer": "B",
            },
            {
                "prompt": "In 1492, how many people were probably in the Americas?",
                "options": {
                    "A": "Fewer than thirty million",
                    "B": "Exactly thirty million",
                    "C": "Forty million or fewer",
                    "D": "At least forty million",
                },
                "correct_answer": "C",
            },
            {
                "prompt": 'The word "refute" in line 3 is closest in meaning to',
                "options": {"A": "theorize", "B": "support", "C": "contradict", "D": "defend"},
                "correct_answer": "C",
            },
            {
                "prompt": "It is implied in the passage that",
                "options": {
                    "A": "Columbus was really the first person in America",
                    "B": "scientists are sure about America's first inhabitants",
                    "C": "Columbus arrived at almost the same time as America's first inhabitants",
                    "D": "all is not known about America's first inhabitants",
                },
                "correct_answer": "D",
            },
            {
                "prompt": "There is general agreement that the first people who came to North America came from",
                "options": {"A": "Europe", "B": "South America", "C": "northeastern Asia", "D": "Africa"},
                "correct_answer": "C",
            },
            {
                "prompt": 'The word "considerable" in line 6 could best be replaced by which of the following?',
                "options": {"A": "Large", "B": "Weak", "C": "Well-known", "D": "Considerate"},
                "correct_answer": "A",
            },
            {
                "prompt": 'The word "separates" in line 9 is closest in meaning to',
                "options": {"A": "differentiates", "B": "divides", "C": "joins", "D": "crosses"},
                "correct_answer": "B",
            },
            {
                "prompt": "Which of the following is NOT stated about the Bering Strait?",
                "options": {
                    "A": "It is 55 miles wide.",
                    "B": "It separates North America and Asia.",
                    "C": "It was probably a land bridge during the Ice Ages.",
                    "D": "It is a land bridge today.",
                },
                "correct_answer": "D",
            },
            {
                "prompt": 'The word "frozen" in line 11 could best be replaced by',
                "options": {"A": "cool", "B": "dirty", "C": "solid", "D": "wet"},
                "correct_answer": "C",
            },
            {
                "prompt": "Where in the passage does the author mention how long people have probably been in the Americas?",
                "options": {"A": "Lines 1-2", "B": "Lines 3-4", "C": "Lines 6-7", "D": "Lines 8-9"},
                "correct_answer": "C",
            },
        ],
    },
    {
        "title": "Alpha Centauri",
        "text": (
            "Alpha Centauri is a triple-star system. One of the three stars in "
            "Alpha Centauri is Proxima Centauri, which is the nearest star to the "
            'Earth, except of course for the Sun. The name "Proxima" comes from a '
            'Latin word which means "close."\n\n'
            "Even though Proxima Centauri is the closest star to the Earth outside "
            "of our solar system, it is not really close. Interstellar distances "
            "are so large that they are almost impossible to imagine. A person "
            "traveling in a modern spacecraft would not arrive at Proxima Centauri "
            "within this lifetime, or the next, or even ten lifetimes because the "
            "distance is so great. Light travels at a speed of 186,000 miles per "
            "second, and it still takes light more than four years to travel from "
            "Proxima Centauri to the Earth.\n\n"
            "Alpha Centauri can be easily seen in the night sky without a telescope "
            "from certain parts of the Earth. It is the third brightest star in the "
            "sky, out of approximately 6,000 visible stars. It cannot be seen from "
            "most parts of the United States because most of the United States is "
            "too far north; however, it can be seen from the southern parts of the "
            "southernmost states."
        ),
        "questions": [
            {
                "prompt": "The main subject of this passage is",
                "options": {
                    "A": "the closest stars to the Earth",
                    "B": "modern space travel",
                    "C": "the speed of light",
                    "D": "interstellar distances",
                },
                "correct_answer": "D",
            },
            {
                "prompt": "The passage indicates that which of the following is NOT true?",
                "options": {
                    "A": "Alpha Centauri is composed of three stars.",
                    "B": "Proxima Centauri is the closest star to the Earth.",
                    "C": "Proxima Centauri is one of the stars in Alpha Centauri.",
                    "D": "It is possible to see Alpha Centauri from the Earth.",
                },
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "comes" in line 3 could best be replaced by',
                "options": {"A": "travels", "B": "is derived", "C": "is directed", "D": "visits"},
                "correct_answer": "B",
            },
            {
                "prompt": '"Interstellar distances" in line 5 are',
                "options": {
                    "A": "distances between stars",
                    "B": "distances between the Earth and various stars",
                    "C": "distances measured by the speed of light",
                    "D": "distances from the Sun to each of the planets, including the Earth",
                },
                "correct_answer": "A",
            },
            {
                "prompt": (
                    "It can be inferred from the passage that if a person left in one "
                    "of today's spacecrafts, he or she would arrive at Alpha Centauri"
                ),
                "options": {
                    "A": "within this lifetime",
                    "B": "within the next lifetime",
                    "C": "within ten lifetimes",
                    "D": "after more than ten lifetimes",
                },
                "correct_answer": "D",
            },
            {
                "prompt": 'The word "great" in line 7 could best be replaced by which of the following?',
                "options": {"A": "Famous", "B": "Well-known", "C": "Accomplished", "D": "Big"},
                "correct_answer": "D",
            },
            {
                "prompt": "Which of the following is true according to the passage?",
                "options": {
                    "A": "Light travels at 186,000 miles per hour.",
                    "B": "A person could travel from Earth to Proxima Centauri in four years.",
                    "C": "Light from Proxima Centauri reaches the Earth in four years.",
                    "D": "It is 186,000 miles from the Earth to Proxima Centauri.",
                },
                "correct_answer": "C",
            },
            {
                "prompt": 'The word "brightest" in line 11 could best be replaced by',
                "options": {"A": "smartest", "B": "palest", "C": "shiniest", "D": "largest"},
                "correct_answer": "C",
            },
            {
                "prompt": "It can be inferred from the passage that from Alaska Alpha Centauri is",
                "options": {"A": "always visible", "B": "frequently visible", "C": "occasionally visible", "D": "never visible"},
                "correct_answer": "D",
            },
            {
                "prompt": "Where in the passage does the author explain how fast light can travel?",
                "options": {"A": "Lines 1-2", "B": "Line 5", "C": "Lines 7-9", "D": "Lines 10-11"},
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
        print(f"{inserted} preguntas de Reading insertadas en {len(PASSAGES)} passages. Sin skills.")


if __name__ == "__main__":
    seed()
