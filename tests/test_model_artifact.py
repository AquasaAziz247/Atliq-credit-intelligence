import joblib
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.baseline_experiment import FEATURES
from src import model_artifact
from src.model_artifact import (
    generate_model_artifact,
    load_model_artifact,
    validate_model_pipeline,
)
from src.model_inference import predict_positive_probability


@pytest.fixture
def fitted_model():
    X = pd.DataFrame(
        {
            "age": [22, 28, 35, 45, 52, 60],
            "income": [18000, 25000, 35000, 50000, 65000, 80000],
            "number_of_dependants": [0, 1, 2, 1, 3, 2],
            "years_at_current_address": [1, 3, 5, 8, 10, 15],
            "bank_balance_at_application": [2000, 5000, 8000, 12000, 18000, 25000],
        },
        columns=FEATURES,
    )
    y = [False, False, False, True, True, True]
    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(random_state=42)),
        ]
    )
    model.fit(X, y)
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
        },
        columns=FEATURES,
    )


def test_generated_artifact_can_be_loaded_and_used(
    tmp_path, fitted_model, valid_input, monkeypatch
):
    raw_files = [tmp_path / "customers.csv", tmp_path / "loans.csv"]
    for path in raw_files:
        path.write_text("synthetic test placeholder", encoding="utf-8")

    monkeypatch.setattr(model_artifact, "REQUIRED_RAW_FILES", tuple(raw_files))
    monkeypatch.setattr(model_artifact, "train_inference_model", lambda: fitted_model)
    artifact_path = tmp_path / "models" / "model.joblib"

    saved_path = generate_model_artifact(artifact_path)
    loaded = load_model_artifact(saved_path)
    probabilities = predict_positive_probability(loaded, valid_input)

    assert saved_path == artifact_path
    assert isinstance(loaded, Pipeline)
    assert len(probabilities) == 1
    assert 0 <= probabilities[0] <= 1


def test_missing_artifact_has_local_generation_instructions(tmp_path):
    missing = tmp_path / "not-generated.joblib"

    with pytest.raises(FileNotFoundError, match="python -m src.model_artifact"):
        load_model_artifact(missing)


def test_artifact_loader_rejects_non_pipeline_artifact(tmp_path):
    invalid_path = tmp_path / "invalid.joblib"
    joblib.dump({"not": "a pipeline"}, invalid_path)

    with pytest.raises(ValueError, match="must contain a scikit-learn Pipeline"):
        load_model_artifact(invalid_path)


def test_artifact_generation_fails_clearly_when_raw_csv_missing(
    tmp_path, monkeypatch
):
    missing_files = (tmp_path / "customers.csv", tmp_path / "loans.csv")
    monkeypatch.setattr(model_artifact, "REQUIRED_RAW_FILES", missing_files)

    with pytest.raises(FileNotFoundError, match="required source CSV"):
        generate_model_artifact(tmp_path / "model.joblib")


def test_pipeline_validator_rejects_unexpected_steps():
    model = Pipeline([("classifier", LogisticRegression())])

    with pytest.raises(ValueError, match="exactly the 'scaler' and 'classifier'"):
        validate_model_pipeline(model)
