"""
Carga las preguntas de Reading Comprehension del POST-TEST (TOEFL POST-TEST)
extraidas de LONGMAN_INTRODUCTORY_COURSE_PART2_PART3.pdf (paginas 198-207):
5 passages, 50 preguntas. Mismas advertencias: verified=False, sin skills.

Este es el ultimo bloque de seed: al correr los 8 scripts en orden, el
Question Bank queda completo con las 360 preguntas de ambos PDFs.

Uso:
    python -m scripts.seed_longman_reading_posttest
"""
from sqlmodel import Session

from app.core.database import engine
from app.modules.question_bank.models import Passage, Question, QuestionType, Section

SOURCE = "LONGMAN_INTRODUCTORY_COURSE_PART2_PART3.pdf - Reading Comprehension Post-Test / TOEFL POST-TEST (p.198-207)"

PASSAGES = [
    {
        "title": "The Bee Hummingbird",
        "text": (
            "The tiniest bird in the world is the male bee hummingbird. Because it "
            "is so small, it is often mistaken for a bee or some other type of "
            "insect of that size.\n\n"
            "As a hummingbird, it is able to flap its wings extremely quickly, up "
            "to eighty times per second. With this really fast wing speed, the bee "
            "hummingbird can hover like a helicopter, fly forward, fly backward, or "
            "even fly upside down."
        ),
        "questions": [
            {
                "prompt": "What is the topic of this passage?",
                "options": {"A": "The bee", "B": "One type of hummingbird", "C": "How fast hummingbirds fly", "D": "How helicopters fly"},
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "tiniest" in line 1 is closest in meaning to',
                "options": {"A": "fastest", "B": "most dangerous", "C": "noisiest", "D": "smallest"},
                "correct_answer": "D",
            },
            {
                "prompt": "It can be inferred from the passage that the female bee hummingbird",
                "options": {
                    "A": "is really a bee",
                    "B": "does not exist",
                    "C": "is larger than the male",
                    "D": "eats insects",
                },
                "correct_answer": "C",
            },
            {
                "prompt": "According to the passage, when people see a male bee hummingbird, they often incorrectly think it is",
                "options": {"A": "a bird", "B": "an insect", "C": "a bat", "D": "a helicopter"},
                "correct_answer": "B",
            },
            {
                "prompt": 'In line 3, to "flap" wings is to',
                "options": {"A": "hold them still", "B": "stretch them out", "C": "fold them", "D": "move them up and down"},
                "correct_answer": "D",
            },
            {
                "prompt": "According to the passage, how fast can a bee hummingbird flap its wings?",
                "options": {"A": "A hundred times each second", "B": "Eighty times per minute", "C": "Eighty times each second", "D": "Eight times in a second"},
                "correct_answer": "C",
            },
            {
                "prompt": 'In line 4, to "hover" is to',
                "options": {"A": "fly forward quickly", "B": "land", "C": "stay in place in the air", "D": "use fuel"},
                "correct_answer": "C",
            },
            {
                "prompt": "The passage indicates that a bee hummingbird can do all of the following EXCEPT",
                "options": {"A": "hover", "B": "fly backward", "C": "fly in an inverted position", "D": "fly a helicopter"},
                "correct_answer": "D",
            },
        ],
    },
    {
        "title": "Elephant Communication",
        "text": (
            "One mystery about elephants that seems to have been solved is how "
            "elephants communicate with each other. Humans have heard a whole "
            "variety of sounds coming from elephants, but these sounds are not the "
            "only way that elephants communicate.\n\n"
            "A new explanation about elephant communication is being proposed. "
            "Elephants vibrate the air in their trunks and foreheads. The sound "
            "that is created during this vibration has an extremely low pitch; the "
            "pitch, in fact, is so low that humans cannot hear it. However, it "
            "seems that other elephants can and do hear and understand these low "
            "rumblings."
        ),
        "questions": [
            {
                "prompt": "The passage mainly discusses",
                "options": {
                    "A": "the answer to a question about how elephants communicate",
                    "B": "how elephants vibrate the air in their trunks",
                    "C": "communication between animals and humans",
                    "D": "the sounds that elephants make",
                },
                "correct_answer": "A",
            },
            {
                "prompt": 'A "mystery" in line 1 is',
                "options": {"A": "a speech", "B": "something unknown", "C": "a funny story", "D": "a detective"},
                "correct_answer": "B",
            },
            {
                "prompt": "According to the passage, people",
                "options": {
                    "A": "cannot hear any elephant sounds",
                    "B": "are not interested in elephant sounds",
                    "C": "hear only one elephant sound",
                    "D": "can hear numerous elephant sounds",
                },
                "correct_answer": "D",
            },
            {
                "prompt": "It can be inferred from the passage that the elephant sounds that humans hear are",
                "options": {
                    "A": "one of the ways that elephants communicate",
                    "B": "not part of elephant communication",
                    "C": "how elephants communicate with humans",
                    "D": "the only sounds that elephants make",
                },
                "correct_answer": "A",
            },
            {
                "prompt": 'The word "way" in line 3 could best be replaced by',
                "options": {"A": "direction", "B": "method", "C": "path", "D": "road"},
                "correct_answer": "B",
            },
            {
                "prompt": "Where do elephants vibrate air?",
                "options": {"A": "In their throats", "B": "In their trunks", "C": "In their mouths", "D": "In their ears"},
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "pitch" in line 6 is closest in meaning to which of the following?',
                "options": {"A": "Meaning", "B": "Voice", "C": "Height", "D": "Sound"},
                "correct_answer": "C",
            },
            {
                "prompt": "Which of the following is NOT true about the extremely low sound created by elephants?",
                "options": {
                    "A": "Humans cannot understand it.",
                    "B": "Humans hear it.",
                    "C": "Elephants hear it.",
                    "D": "Elephants understand it.",
                },
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "rumblings" in line 7 is closest in meaning to',
                "options": {"A": "words", "B": "ears", "C": "vibrations", "D": "melodies"},
                "correct_answer": "C",
            },
            {
                "prompt": "Where in the passage does the author describe the sound that elephants create in their trunks and foreheads?",
                "options": {"A": "Lines 1-2", "B": "Lines 2-3", "C": "Line 4", "D": "Lines 5-6"},
                "correct_answer": "D",
            },
        ],
    },
    {
        "title": "George Gershwin",
        "text": (
            "George Gershwin grew up in New York City, and he first made his "
            'living playing popular music on the piano in "Tin Pan Alley," the '
            "music publishing district of New York. It was there that he developed "
            "a strong feel for the popular music of the time that served as a "
            "basis for the popular songs that he composed.\n\n"
            "In addition to his love of popular songs, he enjoyed jazz and believed "
            "that jazz was the primary source of truly American folk music. Jazz "
            "had, prior to Gershwin's time, been performed by small jazz bands and "
            "soloists, but Gershwin believed that jazz could serve as the basis for "
            "serious symphonic works. Gershwin became the link between jazz and "
            "serious classical music with such works as his jazz concerto Rhapsody "
            'in Blue and the jazz-inspired orchestral piece An American in Paris.'
        ),
        "questions": [
            {
                "prompt": "The passage mainly discusses",
                "options": {"A": "George Gershwin's popular music", "B": "Tin Pan Alley", "C": "American jazz", "D": "the variety of music by Gershwin"},
                "correct_answer": "D",
            },
            {
                "prompt": 'The word "made" in line 1 could best be replaced by',
                "options": {"A": "constructed", "B": "earned", "C": "worked", "D": "built"},
                "correct_answer": "B",
            },
            {
                "prompt": "According to the passage, Tin Pan Alley is",
                "options": {"A": "a piano shop", "B": "a music studio", "C": "an area in New York City", "D": "a street where Gershwin lived"},
                "correct_answer": "C",
            },
            {
                "prompt": "Which of the following is NOT true about George Gershwin's relationship with popular music?",
                "options": {
                    "A": "He played popular music on the piano.",
                    "B": "Popular music was the foundation of some of his songs.",
                    "C": "He wrote some popular songs.",
                    "D": "Popular music was the only type of music that he enjoyed.",
                },
                "correct_answer": "D",
            },
            {
                "prompt": "Gershwin believed that jazz",
                "options": {"A": "was real American traditional music", "B": "should only be played in small bands", "C": "was not serious music", "D": "was not as enjoyable as popular music"},
                "correct_answer": "A",
            },
            {
                "prompt": 'The word "primary" in line 5 is closest in meaning to',
                "options": {"A": "main", "B": "only", "C": "first", "D": "unknown"},
                "correct_answer": "A",
            },
            {
                "prompt": 'The expression "prior to" in line 6 is closest in meaning to',
                "options": {"A": "during", "B": "after", "C": "in", "D": "before"},
                "correct_answer": "D",
            },
            {
                "prompt": "It can be inferred from the passage that Gershwin",
                "options": {"A": "wrote the first jazz music", "B": "wrote jazz music for larger groups", "C": "did not like writing jazz music", "D": "wrote only for small jazz bands"},
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "link" in line 8 is closest in meaning to',
                "options": {"A": "divider", "B": "separation", "C": "judge", "D": "connection"},
                "correct_answer": "D",
            },
            {
                "prompt": "Where in the passage does the author mention the names of some of Gershwin's works?",
                "options": {"A": "Lines 1-2", "B": "Lines 2-4", "C": "Lines 5-6", "D": "Lines 8-10"},
                "correct_answer": "D",
            },
        ],
    },
    {
        "title": "Chewing Gum",
        "text": (
            "Like a lot of other ideas, chewing gum developed when an inventive "
            "person was trying to develop something else. In 1870, Thomas Adams "
            "was trying to create a substance similar to rubber. He knew that in "
            "the past, natives of Mexico had enjoyed chewing chicle, which was the "
            "gum of the sapodilla tree; he thought that this chicle might possibly "
            "be useful as a replacement for rubber. While he was working with it, "
            "he decided to try chewing it, just as had been done in Mexico. He "
            "enjoyed the sensation and decided that he should try selling it. "
            "Unfortunately, however, not many people bought it. He then improved "
            "the product by adding flavorings and sugar to it, and he gave out "
            "free samples until the product caught on. Though he never succeeded "
            "in his original search for a replacement for rubber, he became "
            "highly successful as a chewing gum producer."
        ),
        "questions": [
            {
                "prompt": "The main idea of the passage is that",
                "options": {
                    "A": "chicle was commonly chewed in Mexico",
                    "B": "Thomas Adams invented chewing gum by accident",
                    "C": "Thomas Adams enjoyed chewing chicle",
                    "D": "Thomas Adams was unsuccessful in finding a substitute for rubber",
                },
                "correct_answer": "B",
            },
            {
                "prompt": 'In line 1, the expression "an inventive person" could best be replaced by',
                "options": {"A": "a creative person", "B": "an illogical person", "C": "a destructive person", "D": "a mistaken person"},
                "correct_answer": "A",
            },
            {
                "prompt": "According to the passage, what did Thomas Adams originally want to create?",
                "options": {"A": "Chewing gum", "B": "The sapodilla tree", "C": "A rubber substitute", "D": "Flavorings"},
                "correct_answer": "C",
            },
            {
                "prompt": "Which of the following is NOT true about chicle?",
                "options": {
                    "A": "It comes from a tree.",
                    "B": "Some people like chewing it.",
                    "C": "It is part of the rubber plant.",
                    "D": "Adams thought he might find a use for it.",
                },
                "correct_answer": "C",
            },
            {
                "prompt": 'In line 3, "natives" are',
                "options": {"A": "trees", "B": "people", "C": "places", "D": "plastics"},
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "sensation" in line 6 is closest in meaning to',
                "options": {"A": "thought", "B": "feeling", "C": "taste", "D": "look"},
                "correct_answer": "B",
            },
            {
                "prompt": "According to the passage, what happened when Thomas Adams first tried selling his chicle product?",
                "options": {
                    "A": "It did not sell very well.",
                    "B": "It was successful because of the taste.",
                    "C": "People thought it was rubber.",
                    "D": "Adams became immediately successful.",
                },
                "correct_answer": "A",
            },
            {
                "prompt": '"Flavorings" in line 9 are used to improve a product\'s',
                "options": {"A": "appearance", "B": "feel", "C": "taste", "D": "smell"},
                "correct_answer": "C",
            },
            {
                "prompt": "It is implied in the passage that Adams gave out free samples of gum because",
                "options": {
                    "A": "he had a lot that he did not want",
                    "B": "he did not care about making money",
                    "C": "he was not a very smart businessman",
                    "D": "he wanted to improve future sales",
                },
                "correct_answer": "D",
            },
            {
                "prompt": "According to the passage, in his search for a rubber substitute, Adams",
                "options": {"A": "was not successful", "B": "found the original rubber plant", "C": "succeeded late in his life", "D": "was highly successful"},
                "correct_answer": "A",
            },
            {
                "prompt": "Where in the passage does the author explain what chicle is?",
                "options": {"A": "Lines 1-2", "B": "Lines 3-4", "C": "Line 5", "D": "Lines 8-9"},
                "correct_answer": "B",
            },
        ],
    },
    {
        "title": "Dead Mail",
        "text": (
            "Sometimes mail arrives at the post office, and it is impossible to "
            "deliver the mail. Perhaps there is an inadequate or illegible address "
            'and no return address. The post office cannot just throw this mail '
            'away, so this becomes "dead mail." This dead mail is sent to one of '
            "the U.S. Postal Service's dead-mail offices in Atlanta, New York, "
            "Philadelphia, St. Paul, or San Francisco. Seventy-five million pieces "
            "of mail can end up in the dead-mail office in one year.\n\n"
            "The staff of the dead-mail offices have a variety of ways to deal "
            "with all of these pieces of dead mail. First of all, they look for "
            "clues that can help them deliver the mail; they open packages in the "
            "hope that something inside will show where the package came from or "
            "is going to. Dead mail will also be listed on a computer so that "
            "people can call in and check to see if a missing item is there.\n\n"
            "However, all of this mail cannot simply be stored forever; there is "
            "just too much of it. When a lot of dead mail has piled up, the "
            "dead-mail offices hold public auctions. Every three months, the "
            "public is invited in and bins containing items found in dead-mail "
            "packages are sold to the highest bidder."
        ),
        "questions": [
            {
                "prompt": "The best title for the passage is",
                "options": {"A": "The U.S. Postal Service", "B": "Staff Responsibilities at the U.S. Postal Service", "C": "Why Mail Is Undeliverable", "D": "Dead-Mail Offices"},
                "correct_answer": "D",
            },
            {
                "prompt": "Dead mail is mail that",
                "options": {"A": "has no use", "B": "has been read and thrown away", "C": "is unwanted", "D": "is undeliverable"},
                "correct_answer": "D",
            },
            {
                "prompt": 'The word "illegible" in line 2 is closest in meaning to which of the following?',
                "options": {"A": "Incomplete", "B": "Missing", "C": "Unreadable", "D": "Incorrect"},
                "correct_answer": "C",
            },
            {
                "prompt": "According to the passage, how many dead-mail offices does the U.S. Postal Service have?",
                "options": {"A": "3", "B": "5", "C": "15", "D": "75"},
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "staff" in line 6 is closest in meaning to',
                "options": {"A": "workers", "B": "machines", "C": "rules", "D": "pieces of furniture"},
                "correct_answer": "A",
            },
            {
                "prompt": "Which of the following is NOT mentioned as a way that post office staff members deal with dead mail?",
                "options": {"A": "They search for clues.", "B": "They throw dead mail away.", "C": "They open dead mail.", "D": "They list dead mail on a computer."},
                "correct_answer": "B",
            },
            {
                "prompt": "It is implied in the passage that the dead-mail staff would be happy if they opened a package and found",
                "options": {"A": "money", "B": "jewelry", "C": "a computer", "D": "an address"},
                "correct_answer": "D",
            },
            {
                "prompt": 'The expression "call in" in line 9 could best be replaced by',
                "options": {"A": "visit", "B": "phone", "C": "shout", "D": "talk"},
                "correct_answer": "B",
            },
            {
                "prompt": 'The word "auctions" in line 11 is closest in meaning to',
                "options": {"A": "sales", "B": "deliveries", "C": "meetings", "D": "demonstrations"},
                "correct_answer": "A",
            },
            {
                "prompt": "The passage indicates that dead-mail auctions are held",
                "options": {"A": "once a year", "B": "twice a year", "C": "three times a year", "D": "four times a year"},
                "correct_answer": "D",
            },
            {
                "prompt": "Where in the passage does the author explain why the post office cannot store dead mail forever?",
                "options": {"A": "Lines 2-3", "B": "Lines 4-5", "C": "Lines 7-8", "D": "Line 10"},
                "correct_answer": "D",
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
