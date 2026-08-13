"""
Vocabulario academico nivel TOEFL ITP (objetivo 550 puntos).

A diferencia de los demas seeds, este contenido NO viene de los PDFs
fuente (ninguno de los dos trae una seccion de vocabulario independiente
del Reading). Es contenido ORIGINAL, escrito para este proyecto siguiendo
el mismo formato "palabra en contexto -> sinonimo mas cercano" que ya
usan las preguntas de vocabulario dentro de Reading.

verified=True aqui significa "este es el contenido definitivo que
Claude genero para el proyecto" -- no aplica el mismo sentido de
"verificado contra el answer key del libro" que en los demas seeds,
porque no hay libro del que verificar.

Uso:
    python -m scripts.seed_vocabulary
"""
from sqlmodel import Session

from app.core.database import engine
from app.modules.question_bank.models import Question, QuestionType, Section

SOURCE = "Contenido original generado por Claude para UPMH English Prep - Vocabulario académico TOEFL ITP (nivel 550)"

VOCABULARY_QUESTIONS = [
    {
        "prompt": 'The committee\'s decision to postpone the vote was <u>arbitrary</u>, with no clear reasoning provided.',
        "options": {"A": "unanimous", "B": "random", "C": "delayed", "D": "official"},
        "correct_answer": "B",
        "explanation": "'Arbitrary' significa basado en el capricho o azar, no en razón ni sistema — el sinónimo más cercano es 'random'.",
    },
    {
        "prompt": 'Despite the researchers\' efforts, the results remained <u>ambiguous</u> and open to multiple interpretations.',
        "options": {"A": "unclear", "B": "conclusive", "C": "surprising", "D": "irrelevant"},
        "correct_answer": "A",
        "explanation": "'Ambiguous' significa que algo se puede interpretar de más de una manera, es decir, poco claro.",
    },
    {
        "prompt": 'The professor asked students to <u>corroborate</u> their claims with evidence from at least two sources.',
        "options": {"A": "abandon", "B": "confirm", "C": "publish", "D": "translate"},
        "correct_answer": "B",
        "explanation": "'Corroborate' significa apoyar o confirmar una afirmación con evidencia adicional.",
    },
    {
        "prompt": 'The explanation, though <u>plausible</u>, was never tested experimentally.',
        "options": {"A": "believable", "B": "outdated", "C": "complicated", "D": "incorrect"},
        "correct_answer": "A",
        "explanation": "'Plausible' significa que algo parece razonable o creíble, aunque no esté comprobado.",
    },
    {
        "prompt": 'The new regulation is expected to <u>mitigate</u> the environmental impact of the factory.',
        "options": {"A": "eliminate", "B": "reduce", "C": "publicize", "D": "cause"},
        "correct_answer": "B",
        "explanation": "'Mitigate' significa suavizar o reducir la severidad de algo, no eliminarlo por completo.",
    },
    {
        "prompt": 'Water scarcity is a <u>prevalent</u> issue in many regions of the world.',
        "options": {"A": "recent", "B": "minor", "C": "widespread", "D": "debated"},
        "correct_answer": "C",
        "explanation": "'Prevalent' significa común o extendido en un área o momento determinado.",
    },
    {
        "prompt": 'Given the current budget, expanding the program this year is not <u>feasible</u>.',
        "options": {"A": "possible", "B": "popular", "C": "necessary", "D": "profitable"},
        "correct_answer": "A",
        "explanation": "'Feasible' significa que algo se puede realizar o llevar a cabo; 'not feasible' = no es posible.",
    },
    {
        "prompt": 'Auditors noted a significant <u>discrepancy</u> between the reported and actual figures.',
        "options": {"A": "similarity", "B": "difference", "C": "delay", "D": "improvement"},
        "correct_answer": "B",
        "explanation": "'Discrepancy' significa una diferencia o falta de coincidencia entre dos cosas que deberían coincidir.",
    },
    {
        "prompt": 'Some critics argue that the essay contains <u>redundant</u> information that could be removed.',
        "options": {"A": "unnecessary", "B": "false", "C": "confidential", "D": "technical"},
        "correct_answer": "A",
        "explanation": "'Redundant' significa innecesario porque se repite o no añade valor nuevo.",
    },
    {
        "prompt": 'Once the process begins, the outcome becomes essentially <u>inevitable</u>.',
        "options": {"A": "unpredictable", "B": "reversible", "C": "unavoidable", "D": "gradual"},
        "correct_answer": "C",
        "explanation": "'Inevitable' significa que no se puede evitar, que va a suceder de todas formas.",
    },
    {
        "prompt": 'The findings of the first study were confirmed by a <u>subsequent</u> investigation.',
        "options": {"A": "earlier", "B": "later", "C": "foreign", "D": "unofficial"},
        "correct_answer": "B",
        "explanation": "'Subsequent' significa que ocurre después, posterior en el tiempo.",
    },
    {
        "prompt": 'The report offers a <u>comprehensive</u> overview of the region\'s economic history.',
        "options": {"A": "brief", "B": "biased", "C": "complete", "D": "outdated"},
        "correct_answer": "C",
        "explanation": "'Comprehensive' significa completo, que abarca todos o casi todos los aspectos relevantes.",
    },
    {
        "prompt": 'The results should be considered <u>tentative</u> until the full data set has been analyzed.',
        "options": {"A": "final", "B": "provisional", "C": "invalid", "D": "public"},
        "correct_answer": "B",
        "explanation": "'Tentative' significa provisional o sujeto a cambios, no definitivo.",
    },
    {
        "prompt": 'The company reported a <u>substantial</u> increase in revenue this quarter.',
        "options": {"A": "slight", "B": "unexpected", "C": "considerable", "D": "temporary"},
        "correct_answer": "C",
        "explanation": "'Substantial' significa considerable o de tamaño/importancia notable.",
    },
    {
        "prompt": 'Curiosity is an <u>inherent</u> trait in young children, not something they are taught.',
        "options": {"A": "rare", "B": "natural", "C": "harmful", "D": "temporary"},
        "correct_answer": "B",
        "explanation": "'Inherent' significa que forma parte esencial de algo desde el principio, es decir, natural o innato.",
    },
    {
        "prompt": 'The theory is based on <u>empirical</u> evidence gathered over several decades of observation.',
        "options": {"A": "theoretical", "B": "observed", "C": "outdated", "D": "controversial"},
        "correct_answer": "B",
        "explanation": "'Empirical' significa basado en la observación o experiencia directa, no solo en teoría.",
    },
    {
        "prompt": 'One <u>salient</u> feature of the design is its unusually low energy consumption.',
        "options": {"A": "hidden", "B": "prominent", "C": "expensive", "D": "recent"},
        "correct_answer": "B",
        "explanation": "'Salient' significa notable o que destaca claramente por encima de otros aspectos.",
    },
    {
        "prompt": 'Prolonged drought can <u>exacerbate</u> existing food shortages in the region.',
        "options": {"A": "worsen", "B": "solve", "C": "delay", "D": "explain"},
        "correct_answer": "A",
        "explanation": "'Exacerbate' significa empeorar o intensificar un problema existente.",
    },
    {
        "prompt": 'A stable political environment is generally <u>conducive</u> to economic growth.',
        "options": {"A": "harmful", "B": "irrelevant", "C": "favorable", "D": "opposed"},
        "correct_answer": "C",
        "explanation": "'Conducive to' significa que favorece o facilita que algo ocurra.",
    },
    {
        "prompt": 'Solar power is becoming an increasingly <u>viable</u> alternative to fossil fuels.',
        "options": {"A": "expensive", "B": "workable", "C": "controversial", "D": "temporary"},
        "correct_answer": "B",
        "explanation": "'Viable' significa que puede funcionar o tener éxito en la práctica.",
    },
    {
        "prompt": 'Crop yields were <u>meager</u> this year due to the unusually dry summer.',
        "options": {"A": "abundant", "B": "scarce", "C": "delayed", "D": "profitable"},
        "correct_answer": "B",
        "explanation": "'Meager' significa escaso o insuficiente en cantidad.",
    },
    {
        "prompt": 'The bridge was engineered to be <u>robust</u> enough to withstand extreme weather.',
        "options": {"A": "fragile", "B": "strong", "C": "affordable", "D": "temporary"},
        "correct_answer": "B",
        "explanation": "'Robust' significa fuerte, resistente o difícil de dañar.",
    },
    {
        "prompt": 'The library is <u>adjacent</u> to the main administration building.',
        "options": {"A": "identical", "B": "opposite", "C": "next to", "D": "far from"},
        "correct_answer": "C",
        "explanation": "'Adjacent' significa contiguo o al lado de algo.",
    },
    {
        "prompt": 'Biologists must carefully <u>differentiate</u> between similar species based on subtle traits.',
        "options": {"A": "combine", "B": "distinguish", "C": "classify alphabetically", "D": "ignore"},
        "correct_answer": "B",
        "explanation": "'Differentiate' significa distinguir o notar las diferencias entre cosas similares.",
    },
    {
        "prompt": 'The scientist proposed a new <u>hypothesis</u> to explain the unexpected data.',
        "options": {"A": "law", "B": "conclusion", "C": "proposed explanation", "D": "measurement"},
        "correct_answer": "C",
        "explanation": "'Hypothesis' es una explicación propuesta que aún debe probarse, no una conclusión definitiva.",
    },
    {
        "prompt": 'The report attempts to <u>delineate</u> the boundaries between public and private land.',
        "options": {"A": "blur", "B": "define clearly", "C": "sell", "D": "expand"},
        "correct_answer": "B",
        "explanation": "'Delineate' significa describir o marcar los límites de algo con precisión.",
    },
    {
        "prompt": 'Researchers found that income and education levels strongly <u>correlate</u> in this population.',
        "options": {"A": "are related", "B": "are opposed", "C": "are irrelevant", "D": "are equal"},
        "correct_answer": "A",
        "explanation": "'Correlate' significa que dos variables están relacionadas o varían juntas.",
    },
    {
        "prompt": 'After years under foreign rule, the territory finally became <u>autonomous</u>.',
        "options": {"A": "poor", "B": "self-governing", "C": "divided", "D": "unstable"},
        "correct_answer": "B",
        "explanation": "'Autonomous' significa que se gobierna a sí mismo, independiente de control externo.",
    },
    {
        "prompt": 'The judge\'s ruling set an important legal <u>precedent</u> for future cases.',
        "options": {"A": "exception", "B": "prior example used as a guide", "C": "punishment", "D": "requirement"},
        "correct_answer": "B",
        "explanation": "'Precedent' es un caso o decisión anterior que sirve de referencia para casos futuros similares.",
    },
    {
        "prompt": 'She felt <u>ambivalent</u> about the job offer, seeing both strong advantages and drawbacks.',
        "options": {"A": "excited", "B": "uncertain, with mixed feelings", "C": "confident", "D": "indifferent"},
        "correct_answer": "B",
        "explanation": "'Ambivalent' significa tener sentimientos encontrados o contradictorios sobre algo.",
    },
    {
        "prompt": 'The sudden drop in temperature was an <u>anomaly</u> for that time of year.',
        "options": {"A": "an irregularity", "B": "a tradition", "C": "an improvement", "D": "a forecast"},
        "correct_answer": "A",
        "explanation": "'Anomaly' significa algo que se desvía de lo normal o esperado.",
    },
    {
        "prompt": 'The manager took a <u>pragmatic</u> approach, focusing on what would actually work rather than ideals.',
        "options": {"A": "theoretical", "B": "practical", "C": "emotional", "D": "cautious"},
        "correct_answer": "B",
        "explanation": "'Pragmatic' significa práctico, orientado a resultados concretos más que a principios abstractos.",
    },
    {
        "prompt": 'The critique was <u>superficial</u>, failing to engage with the article\'s deeper arguments.',
        "options": {"A": "harsh", "B": "shallow", "C": "detailed", "D": "anonymous"},
        "correct_answer": "B",
        "explanation": "'Superficial' significa que solo aborda la superficie de un tema, sin profundidad.",
    },
    {
        "prompt": 'Only sources considered <u>credible</u> were included in the final bibliography.',
        "options": {"A": "trustworthy", "B": "recent", "C": "expensive", "D": "popular"},
        "correct_answer": "A",
        "explanation": "'Credible' significa digno de confianza o creíble.",
    },
    {
        "prompt": 'Security staff remained <u>vigilant</u> throughout the entire event.',
        "options": {"A": "relaxed", "B": "watchful", "C": "hidden", "D": "organized"},
        "correct_answer": "B",
        "explanation": "'Vigilant' significa alerta y atento a posibles problemas o peligros.",
    },
    {
        "prompt": 'The argument, while <u>coherent</u>, relied on assumptions that were never proven.',
        "options": {"A": "logically consistent", "B": "popular", "C": "brief", "D": "controversial"},
        "correct_answer": "A",
        "explanation": "'Coherent' significa lógicamente consistente y fácil de seguir.",
    },
    {
        "prompt": 'The debate over funding for the project sparked considerable <u>controversy</u> among faculty.',
        "options": {"A": "agreement", "B": "disagreement", "C": "curiosity", "D": "celebration"},
        "correct_answer": "B",
        "explanation": "'Controversy' significa desacuerdo o disputa pública sobre un tema.",
    },
    {
        "prompt": 'The museum\'s collection is <u>notable</u> for its rare medieval manuscripts.',
        "options": {"A": "criticized", "B": "worth noting", "C": "expanded", "D": "borrowed"},
        "correct_answer": "B",
        "explanation": "'Notable' significa digno de atención o mención especial.",
    },
    {
        "prompt": 'Such practices are now <u>ubiquitous</u> in modern manufacturing.',
        "options": {"A": "rare", "B": "present everywhere", "C": "expensive", "D": "forbidden"},
        "correct_answer": "B",
        "explanation": "'Ubiquitous' significa que está presente en todas partes, omnipresente.",
    },
    {
        "prompt": 'The technician was praised for being extremely <u>meticulous</u> in checking every detail.',
        "options": {"A": "careless", "B": "careful and precise", "C": "fast", "D": "friendly"},
        "correct_answer": "B",
        "explanation": "'Meticulous' significa extremadamente cuidadoso y atento a los detalles.",
    },
]


def seed() -> None:
    with Session(engine) as session:
        inserted = 0
        for item in VOCABULARY_QUESTIONS:
            session.add(
                Question(
                    section=Section.vocabulary,
                    question_type=QuestionType.vocabulary_choice,
                    prompt=item["prompt"],
                    options=item["options"],
                    correct_answer=item["correct_answer"],
                    verified=True,  # contenido original, no requiere verificacion contra un libro
                    explanation=item.get("explanation"),
                    source=SOURCE,
                )
            )
            inserted += 1

        session.commit()
        print(f"{inserted} preguntas de vocabulario (contenido original) insertadas.")


if __name__ == "__main__":
    seed()
