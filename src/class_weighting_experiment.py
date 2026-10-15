"""Controlled validation comparison of Logistic Regression class weights.

This educational experiment classifies supplied labels. It does not establish
that the target represents future defaults or that features are point-in-time
safe. The held-out test partition is reserved and is not evaluated here.
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.baseline_experiment import (
    FEATURES,
    RANDOM_STATE,
    TEST_SIZE,
    load_experiment_data,
)

THRESHOLDS = (0.50, 0.075)


def make_logistic_pipeline(class_weight=None) -> Pipeline:
    """Build the same scaled Logistic Regression pipeline for each variant."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=RANDOM_STATE,
                    class_weight=class_weight,
                ),
            ),
        ]
    )


def make_experiment_splits(X, y):
    """Create fixed fit, validation, and reserved test partitions."""
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    X_fit, X_validation, y_fit, y_validation = train_test_split(
        X_train,
        y_train,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y_train,
    )

    return X_fit, X_validation, y_fit, y_validation, X_test, y_test


def evaluate_at_threshold(
    model_name,
    model,
    X_validation,
    y_validation,
    threshold,
):
    """Calculate validation metrics at one fixed classification threshold."""
    classifier = model.named_steps["classifier"]
    classes = list(classifier.classes_)
    if True not in classes:
        raise ValueError("The fitted classifier has no True positive class.")

    positive_index = classes.index(True)
    probabilities = model.predict_proba(X_validation)[:, positive_index]
    predictions = probabilities >= threshold

    precision = precision_score(
        y_validation, predictions, pos_label=True, zero_division=0
    )
    recall = recall_score(
        y_validation, predictions, pos_label=True, zero_division=0
    )
    f1 = f1_score(
        y_validation, predictions, pos_label=True, zero_division=0
    )
    auc = roc_auc_score(y_validation, probabilities)
    matrix = confusion_matrix(
        y_validation, predictions, labels=[False, True]
    )

    result = {
        "Model": model_name,
        "Threshold": threshold,
        "ROC-AUC": auc,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "Predicted positives": int(predictions.sum()),
        "Predicted-positive proportion": float(predictions.mean()),
    }
    return result, matrix


def run_experiment():
    """Fit both variants on identical fit rows and compare validation results."""
    X, y = load_experiment_data()

    if list(X.columns) != FEATURES:
        raise ValueError("Loaded features do not match the approved allowlist.")

    (
        X_fit,
        X_validation,
        y_fit,
        y_validation,
        X_reserved_test,
        y_reserved_test,
    ) = make_experiment_splits(X, y)

    # The test partition is deliberately not used for fitting or evaluation.
    print("=== DAY 10 CLASS-WEIGHTING EXPERIMENT ===")
    print("Educational classification of supplied labels only.")
    print("Approved features:", FEATURES)
    print(f"Fit rows: {len(X_fit)}")
    print(f"Validation rows: {len(X_validation)}")
    print(f"Reserved test rows: {len(X_reserved_test)}")
    print("Reserved test labels will not be evaluated.")
    print(f"Fit positive-label rate: {y_fit.mean():.6f}")
    print(f"Validation positive-label rate: {y_validation.mean():.6f}")

    configurations = [
        ("Logistic Regression baseline", None),
        ("Logistic Regression balanced", "balanced"),
    ]

    results = []
    for model_name, class_weight in configurations:
        model = make_logistic_pipeline(class_weight=class_weight)
        model.fit(X_fit, y_fit)

        print(f"\n--- {model_name} ---")
        print(f"class_weight={class_weight!r}")

        for threshold in THRESHOLDS:
            result, matrix = evaluate_at_threshold(
                model_name,
                model,
                X_validation,
                y_validation,
                threshold,
            )
            results.append(result)
            print(f"\nThreshold: {threshold:.3f}")
            print("Confusion matrix (actual rows, predicted columns):")
            print(matrix)

    results_frame = pd.DataFrame(results)
    print("\n=== VALIDATION COMPARISON ===")
    print(results_frame.to_string(index=False, float_format=lambda value: f"{value:.4f}"))

    return results_frame


if __name__ == "__main__":
    run_experiment()
