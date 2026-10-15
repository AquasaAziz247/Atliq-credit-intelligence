import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.baseline_experiment import FEATURES
from src.class_weighting_experiment import (
    THRESHOLDS,
    evaluate_at_threshold,
    make_experiment_splits,
    make_logistic_pipeline,
)


def test_approved_features_and_thresholds_are_fixed():
    assert FEATURES == [
        "age",
        "income",
        "number_of_dependants",
        "years_at_current_address",
        "bank_balance_at_application",
    ]
    assert THRESHOLDS == (0.50, 0.075)


@pytest.mark.parametrize(
    ("class_weight", "expected"),
    [(None, None), ("balanced", "balanced")],
)
def test_pipeline_uses_scaling_and_requested_class_weight(
    class_weight, expected
):
    pipeline = make_logistic_pipeline(class_weight=class_weight)

    assert isinstance(pipeline, Pipeline)
    assert isinstance(pipeline.named_steps["scaler"], StandardScaler)
    assert pipeline.named_steps["classifier"].class_weight == expected
    assert pipeline.named_steps["classifier"].max_iter == 1000


def test_split_sizes_and_partitions_do_not_overlap():
    X = pd.DataFrame(
        {
            feature: np.arange(50_000, dtype=float)
            for feature in FEATURES
        },
        index=np.arange(50_000),
    )
    y = pd.Series(
        np.arange(50_000) % 2 == 0,
        index=X.index,
        name="default",
    )

    X_fit, X_val, y_fit, y_val, X_test, y_test = make_experiment_splits(
        X, y
    )

    assert len(X_fit) == 32_000
    assert len(X_val) == 8_000
    assert len(X_test) == 10_000
    assert len(y_fit) == len(X_fit)
    assert len(y_val) == len(X_val)
    assert len(y_test) == len(X_test)

    fit_ids = set(X_fit.index)
    validation_ids = set(X_val.index)
    test_ids = set(X_test.index)

    assert fit_ids.isdisjoint(validation_ids)
    assert fit_ids.isdisjoint(test_ids)
    assert validation_ids.isdisjoint(test_ids)


def test_evaluation_reports_metrics_and_confusion_matrix():
    from sklearn.linear_model import LogisticRegression

    X = pd.DataFrame(
        {"signal": [-3, -2, -1, 1, 2, 3, -2.5, 2.5]}
    )
    y = pd.Series(
        [False, False, False, True, True, True, False, True]
    )
    model = make_logistic_pipeline()
    model.fit(X, y)

    result, matrix = evaluate_at_threshold(
        "synthetic test model", model, X, y, 0.50
    )

    assert result["Model"] == "synthetic test model"
    assert result["Threshold"] == 0.50
    assert 0.0 <= result["ROC-AUC"] <= 1.0
    assert 0.0 <= result["Precision"] <= 1.0
    assert 0.0 <= result["Recall"] <= 1.0
    assert 0.0 <= result["F1"] <= 1.0
    assert result["Predicted positives"] == int(matrix[:, 1].sum())
    assert result["Predicted-positive proportion"] == pytest.approx(
        result["Predicted positives"] / len(y)
    )
    assert matrix.shape == (2, 2)
    assert matrix.sum() == len(y)


def test_evaluation_rejects_model_without_true_positive_class():
    class FakeModel:
        named_steps = {
            "classifier": type("Classifier", (), {"classes_": np.array([False])})()
        }

    with pytest.raises(ValueError, match="no True positive class"):
        evaluate_at_threshold(
            "invalid model",
            FakeModel(),
            pd.DataFrame({"signal": [0]}),
            pd.Series([False]),
            0.50,
        )
