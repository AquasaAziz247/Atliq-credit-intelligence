import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from src.baseline_experiment import FEATURES
from src.model_inference import predict_positive_probability


@pytest.fixture
def fitted_model():
    """Return a small synthetic model for isolated inference tests."""
    X = pd.DataFrame(
        {
            "age": [22, 28, 35, 45, 52, 60],
            "income": [18000, 25000, 35000, 50000, 65000, 80000],
            "number_of_dependants": [0, 1, 2, 1, 3, 2],
            "years_at_current_address": [1, 3, 5, 8, 10, 15],
            "bank_balance_at_application": [2000, 5000, 8000, 12000, 18000, 25000],
        }
    )
    y = pd.Series([False, False, False, True, True, True])

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(random_state=42)),
        ]
    )
    model.fit(X[FEATURES], y)
    return model


@pytest.fixture
def valid_input():
    return pd.DataFrame(
        {
            "age": [30],
            "income": [40000],
            "number_of_dependants": [1],
            "years_at_current_address": [4],
            "bank_balance_at_application": [9000],
        }
    )


def test_valid_input_returns_probability_between_zero_and_one(
    fitted_model, valid_input
):
    probabilities = predict_positive_probability(fitted_model, valid_input)

    assert len(probabilities) == 1
    assert 0.0 <= probabilities[0] <= 1.0


def test_missing_feature_is_rejected(fitted_model, valid_input):
    invalid = valid_input.drop(columns=["income"])

    with pytest.raises(ValueError, match="Missing required input features"):
        predict_positive_probability(fitted_model, invalid)


def test_non_numeric_input_is_rejected(fitted_model, valid_input):
    invalid = valid_input.copy()
    invalid["income"] = "not-a-number"

    with pytest.raises(ValueError, match="must contain numeric values"):
        predict_positive_probability(fitted_model, invalid)



@pytest.mark.parametrize("bad_value", [np.nan, np.inf, -np.inf])
def test_non_finite_input_is_rejected(fitted_model, valid_input, bad_value):
    invalid = valid_input.copy()
    invalid["income"] = invalid["income"].astype(float)
    invalid.loc[0, "income"] = bad_value

    with pytest.raises(ValueError, match="must not contain missing or infinite"):
        predict_positive_probability(fitted_model, invalid)



def test_empty_input_is_rejected(fitted_model, valid_input):
    empty = valid_input.iloc[0:0]

    with pytest.raises(ValueError, match="At least one input row"):
        predict_positive_probability(fitted_model, empty)


def test_input_dataframe_is_not_modified(fitted_model, valid_input):
    original = valid_input.copy(deep=True)

    predict_positive_probability(fitted_model, valid_input)

    pd.testing.assert_frame_equal(valid_input, original)
