"""
Aproximacion documentada de nivel TOEFL ITP / CEFR -- NO es un score oficial
ETS. Mapea la accuracy sobre evaluaciones completadas linealmente al rango
310-677 (rango real del examen TOEFL ITP) y esa cifra a una banda CEFR por
umbrales aproximados. Funciones puras, sin acceso a DB, para poder ajustarse
o reemplazarse sin tocar las consultas que las alimentan.
"""

TOEFL_SCORE_MIN = 310
TOEFL_SCORE_MAX = 677

# (banda, score_min, score_max) -- aproximacion, no una tabla oficial ETS.
CEFR_BANDS: list[tuple[str, int, int]] = [
    ("A2", 310, 457),
    ("B1", 458, 542),
    ("B2", 543, 626),
    ("C1", 627, 677),
]


def score_from_accuracy(accuracy_ratio: float) -> int:
    accuracy_ratio = max(0.0, min(1.0, accuracy_ratio))
    return round(TOEFL_SCORE_MIN + accuracy_ratio * (TOEFL_SCORE_MAX - TOEFL_SCORE_MIN))


def cefr_band_for_score(score: int) -> tuple[str, float]:
    """Devuelve (banda, porcentaje de avance dentro de esa banda)."""
    for band, band_min, band_max in CEFR_BANDS:
        if band_min <= score <= band_max:
            progress = (score - band_min) / (band_max - band_min) if band_max > band_min else 1.0
            return band, round(progress * 100, 1)

    # Por debajo del piso de la tabla: banda mas baja, 0% de avance.
    return CEFR_BANDS[0][0], 0.0
