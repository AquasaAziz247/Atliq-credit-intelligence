
"""Validate source DataFrames against the project's structural contracts."""

import pandas as pd

from .data_contracts import (
    ALLOWED_MISSINGNESS,
    BUREAU_COLUMNS,
    CUSTOMER_COLUMNS,
    LOAN_COLUMNS,
    PRIMARY_KEYS,
)

REQUIRED_COLUMNS = {
    "customers": CUSTOMER_COLUMNS,
    "loans": LOAN_COLUMNS,
    "bureau": BUREAU_COLUMNS,
}


def validate_schema(df: pd.DataFrame, dataset: str) -> None:
    """Require all expected columns and reject empty datasets."""
    if dataset not in REQUIRED_COLUMNS:
        raise ValueError(f"Unknown dataset contract: {dataset}")

    if df.empty:
        raise ValueError(f"{dataset} dataset must not be empty")

    missing = REQUIRED_COLUMNS[dataset] - set(df.columns)
    if missing:
        raise ValueError(
            f"{dataset} dataset missing required columns: "
            f"{sorted(missing)}"
        )


def validate_missingness(df: pd.DataFrame, dataset: str) -> None:
    """Reject missing values in columns without a documented exception."""
    if dataset not in ALLOWED_MISSINGNESS:
        raise ValueError(f"Unknown dataset contract: {dataset}")

    if df.empty:
        raise ValueError(f"{dataset} dataset must not be empty")

    missing_columns = set(df.columns[df.isna().any()])
    unexpected = missing_columns - ALLOWED_MISSINGNESS[dataset]

    if unexpected:
        details = {
            column: int(df[column].isna().sum())
            for column in sorted(unexpected)
        }
        raise ValueError(
            f"{dataset} dataset has unexpected missing values: {details}"
        )


def validate_dataset_contract(
    df: pd.DataFrame,
    dataset: str,
) -> None:
    """Apply schema, primary-key, and missingness checks."""
    validate_schema(df, dataset)
    validate_missingness(df, dataset)
    validate_primary_key(df, dataset)


def validate_primary_key(df: pd.DataFrame, dataset: str) -> None:
    """Require the configured primary key to be present, complete, unique."""
    if dataset not in PRIMARY_KEYS:
        raise ValueError(f"Unknown dataset contract: {dataset}")

    key = PRIMARY_KEYS[dataset]

    if key not in df.columns:
        raise ValueError(f"{dataset} dataset missing primary key: {key}")

    if df[key].isna().any():
        raise ValueError(f"{dataset}.{key} contains missing values")

    if df[key].duplicated().any():
        raise ValueError(f"{dataset}.{key} contains duplicate values")
