
"""Educational scorecard utilities for AtliQ Credit Intelligence."""

import math


def probability_to_score(probability: float) -> int:
    """Convert a positive-class probability into an educational score."""
    if isinstance(probability, bool) or not isinstance(
        probability, (int, float)
    ):
        raise TypeError("Probability must be a number.")

    if not math.isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError("Probability must be finite and between 0 and 1.")

    return round(900 - 600 * probability)


def score_to_category(score: int) -> str:
    """Map an integer score from 300 to 900 to its category."""
    if isinstance(score, bool) or not isinstance(score, int):
        raise TypeError("Score must be an integer.")

    if not 300 <= score <= 900:
        raise ValueError("Score must be between 300 and 900.")

    if score >= 750:
        return "Excellent"
    if score >= 650:
        return "Good"
    if score >= 500:
        return "Average"
    return "Poor"
