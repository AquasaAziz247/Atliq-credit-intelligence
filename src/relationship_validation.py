
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
    """Require complete child keys to exist in a non-empty, unique parent."""
    if key not in child.columns:
        raise ValueError(f"Child table missing required column: {key}")

    if key not in parent.columns:
        raise ValueError(f"Parent table missing required column: {key}")

    if child.empty:
        raise ValueError("Child table must not be empty")

    if parent.empty:
        raise ValueError("Parent table must not be empty")

    if child[key].isna().any():
        raise ValueError(f"Child key '{key}' contains missing values")

    if parent[key].isna().any():
        raise ValueError(f"Parent key '{key}' contains missing values")

    if parent[key].duplicated().any():
        raise ValueError(f"Parent key '{key}' contains duplicate values")

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
    """Perform a left join only when both sides have complete join keys."""
    if key not in left.columns:
        raise ValueError(f"Left table missing required column: {key}")

    if key not in right.columns:
        raise ValueError(f"Right table missing required column: {key}")

    if left.empty:
        raise ValueError("Left table must not be empty")

    if right.empty:
        raise ValueError("Right table must not be empty")

    if left[key].isna().any():
        raise ValueError(f"Left key '{key}' contains missing values")

    if right[key].isna().any():
        raise ValueError(f"Right key '{key}' contains missing values")

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
    """Require a non-empty target containing only Boolean or integer 0/1."""
    if target not in df.columns:
        raise ValueError(f"Missing target column: {target}")

    if df.empty:
        raise ValueError(f"Target '{target}' must not be empty")

    if df[target].isna().any():
        raise ValueError(f"Target '{target}' contains missing values")

    def is_valid_label(value: object) -> bool:
        # Check Boolean first because bool is a subclass of int in Python.
        if isinstance(value, bool):
            return True

        return isinstance(value, int) and value in (0, 1)

    valid_values = df[target].map(is_valid_label)

    if not valid_values.all():
        raise ValueError(
            f"Target '{target}' must contain only Boolean or integer 0/1 values"
        )
