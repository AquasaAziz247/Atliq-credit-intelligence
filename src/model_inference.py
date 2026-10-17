"""Reusable inference utilities for the educational AtliQ prototype.

Predictions classify the supplied labels. They are not validated estimates
of future default risk or recommendations for real lending decisions.
"""

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.baseline_experiment import FEATURES, load_experiment_data
from src.class_weighting_experiment import (
    make_experiment_splits,
    make_logistic_pipeline,
)


def train_inference_model() -> Pipeline:
    """Fit the baseline pipeline on the established 32,000-row fit split.

    Validation and reserved test partitions are not used for fitting.
    No model-selection decisions are made by this function.
    """
    X, y = load_experiment_data()

    if list(X.columns) != FEATURES:
        raise ValueError("Loaded features do not match the approved feature list.")

    X_fit, _, y_fit, _, _, _ = make_experiment_splits(X, y)

    model = make_logistic_pipeline(class_weight=None)
    model.fit(X_fit, y_fit)
    return model


def predict_positive_probability(
    model: Pipeline,
    inputs: pd.DataFrame,
) -> list[float]:
    """Return positive-class probabilities for validated numeric inputs."""
    if not isinstance(inputs, pd.DataFrame):
        raise TypeError("inputs must be a pandas DataFrame.")

    missing = [feature for feature in FEATURES if feature not in inputs.columns]
    if missing:
        raise ValueError(f"Missing required input features: {missing}")

    if inputs.empty:
        raise ValueError("At least one input row is required.")

    selected = inputs.loc[:, FEATURES].copy()

    for feature in FEATURES:
        try:
            selected[feature] = pd.to_numeric(
                selected[feature], errors="raise"
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Feature '{feature}' must contain numeric values."
            ) from exc

    values = selected.to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Input features must not contain missing or infinite values.")

    classifier = model.named_steps["classifier"]
    classes = list(classifier.classes_)

    if True not in classes:
        raise ValueError("The fitted model has no True positive class.")

    positive_index = classes.index(True)
    probabilities = model.predict_proba(selected)[:, positive_index]

    return probabilities.astype(float).tolist()
