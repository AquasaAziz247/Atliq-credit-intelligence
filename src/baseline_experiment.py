
"""Reproducible educational classification experiment.

This experiment classifies supplied labels. It does not establish that the
labels represent future defaults or that features are available at a verified
prediction time.
"""

from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.relationship_validation import (
    validate_binary_target,
    validated_left_join,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA = PROJECT_ROOT / "data" / "raw"

RANDOM_STATE = 42
TEST_SIZE = 0.20

FEATURES = [
    "age",
    "income",
    "number_of_dependants",
    "years_at_current_address",
    "bank_balance_at_application",
]

TARGET = "default"


def load_experiment_data() -> tuple[pd.DataFrame, pd.Series]:
    """Load the raw tables, validate the join, and select approved columns."""
    customers = pd.read_csv(RAW_DATA / "customers.csv")
    loans = pd.read_csv(RAW_DATA / "loans.csv")

    customer_features = [
        "age",
        "income",
        "number_of_dependants",
        "years_at_current_address",
    ]

    joined = validated_left_join(
        loans,
        customers[["cust_id"] + customer_features],
        key="cust_id",
        validate="one_to_one",
    )

    if len(joined) != len(loans):
        raise ValueError("Customer join unexpectedly changed the row count.")

    if not joined["_merge"].eq("both").all():
        raise ValueError("Customer join contains unmatched loan records.")

    data = joined.drop(columns="_merge")
    validate_binary_target(data, TARGET)

    missing_features = [name for name in FEATURES if name not in data.columns]
    if missing_features:
        raise ValueError(f"Missing approved features: {missing_features}")

    X = data[FEATURES].copy()
    y = data[TARGET].copy()

    if X.isna().any().any():
        raise ValueError("Approved features contain missing values.")

    return X, y


def report_metrics(
    name: str,
    model,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float | str]:
    """Print test metrics and return comparable summary values."""
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)

    print(f"\n=== {name} ===")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 score:  {f1:.4f}")

    print("\nConfusion matrix (actual rows, predicted columns):")
    print(confusion_matrix(y_test, predictions, labels=[False, True]))

    print("\nClassification report:")
    print(classification_report(y_test, predictions, zero_division=0))

    result: dict[str, float | str] = {
        "model": name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, probabilities)
        print(f"ROC-AUC:   {auc:.4f}")
        result["roc_auc"] = auc
    else:
        print("ROC-AUC: not available")

    return result


def main() -> None:
    """Run the dummy baseline and Logistic Regression comparison."""
    X, y = load_experiment_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print("=== EDUCATIONAL LABEL-CLASSIFICATION EXPERIMENT ===")
    print("Not a validated future-default prediction model.")
    print(f"Features: {FEATURES}")
    print(f"Random state: {RANDOM_STATE}")
    print(f"Training rows: {len(X_train)}")
    print(f"Test rows: {len(X_test)}")

    dummy = DummyClassifier(strategy="most_frequent")
    dummy.fit(X_train, y_train)

    logistic_pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )
    logistic_pipeline.fit(X_train, y_train)

    results = [
        report_metrics("DUMMY BASELINE", dummy, X_test, y_test),
        report_metrics("LOGISTIC REGRESSION", logistic_pipeline, X_test, y_test),
    ]

    print("\n=== MODEL COMPARISON ===")
    print(pd.DataFrame(results).to_string(index=False))

    print(
        "\nInterpretation warning: results describe classification of the "
        "supplied labels. Target meaning and feature timing remain unverified."
    )


if __name__ == "__main__":
    main()
