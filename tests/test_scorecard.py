
import math

import pytest

from src.scorecard import probability_to_score, score_to_category


@pytest.mark.parametrize(
    ("probability", "expected_score"),
    [
        (0.0, 900),
        (0.10, 840),
        (0.25, 750),
        (0.50, 600),
        (0.75, 450),
        (1.0, 300),
    ],
)
def test_probability_to_score(probability, expected_score):
    assert probability_to_score(probability) == expected_score


@pytest.mark.parametrize(
    ("score", "expected_category"),
    [
        (900, "Excellent"),
        (750, "Excellent"),
        (749, "Good"),
        (650, "Good"),
        (649, "Average"),
        (500, "Average"),
        (499, "Poor"),
        (300, "Poor"),
    ],
)
def test_score_to_category_boundaries(score, expected_category):
    assert score_to_category(score) == expected_category


@pytest.mark.parametrize("probability", [-0.01, 1.01, math.nan, math.inf, -math.inf])
def test_probability_to_score_rejects_invalid_values(probability):
    with pytest.raises(ValueError):
        probability_to_score(probability)


@pytest.mark.parametrize("probability", [True, False, "0.5", None])
def test_probability_to_score_rejects_non_numeric_types(probability):
    with pytest.raises(TypeError):
        probability_to_score(probability)


@pytest.mark.parametrize("score", [299, 901])
def test_score_to_category_rejects_out_of_range_scores(score):
    with pytest.raises(ValueError):
        score_to_category(score)


@pytest.mark.parametrize("score", [True, 750.0, "750", None])
def test_score_to_category_rejects_non_integer_types(score):
    with pytest.raises(TypeError):
        score_to_category(score)
