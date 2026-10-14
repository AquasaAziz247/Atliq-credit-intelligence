
"""Reusable structural validation for credit-risk source tables."""

import pandas as pd


def validate_key(df: pd.DataFrame, key: str) -> None:
    """Require an existing key column with no missing or duplicate values."""
    if key not in df.columns:
        raise ValueError(f"Missing required key column: {key}")

    if df[key].isna().any():
        raise ValueError(f"Key column '{key}' contains missing values")

    if df[key].duplicated().any():
        raise ValueError(f"Key column '{key}' contains duplicate values")


def validate_referential_integrity(
    child: pd.DataFrame,
    parent: pd.DataFrame,
    key: str = "cust_id",
) -> None:
    """Require every non-missing child key to exist in the parent table."""
    if key not in child.columns:
        raise ValueError(f"Child table missing required column: {key}")

    if key not in parent.columns:
        raise ValueError(f"Parent table missing required column: {key}")

    if child[key].isna().any():
        raise ValueError(f"Child key '{key}' contains missing values")

    if parent[key].isna().any():
        raise ValueError(f"Parent key '{key}' contains missing values")

    unmatched = ~child[key].isin(parent[key])
    if unmatched.any():
        count = int(unmatched.sum())
        raise ValueError(
            f"{count} child rows have '{key}' values absent from parent"
        )


def validated_left_join(
    left: pd.DataFrame,
    right: pd.DataFrame,
    key: str = "cust_id",
    validate: str = "many_to_one",
) -> pd.DataFrame:
    """Perform a left join with explicit cardinality validation."""
    if key not in left.columns:
        raise ValueError(f"Left table missing required column: {key}")

    if key not in right.columns:
        raise ValueError(f"Right table missing required column: {key}")

    return left.merge(
        right,
        on=key,
        how="left",
        validate=validate,
        indicator=True,
    )


def validate_binary_target(
    df: pd.DataFrame,
    target: str = "default",
) -> None:
    """Validate target presence, completeness, and Boolean/binary values."""
    if target not in df.columns:
        raise ValueError(f"Missing target column: {target}")

    if df[target].isna().any():
        raise ValueError(f"Target '{target}' contains missing values")

    valid_values = df[target].isin([True, False, 0, 1])
    if not valid_values.all():
        raise ValueError(
            f"Target '{target}' must contain only Boolean or 0/1 values"
        )
