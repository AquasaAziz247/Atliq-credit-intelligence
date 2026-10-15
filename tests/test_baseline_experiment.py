
import pandas as pd
import pytest

from src.baseline_experiment import FEATURES, load_experiment_data


def test_approved_feature_list_contains_exactly_five_features():
    assert FEATURES == [
        "age",
        "income",
        "number_of_dependants",
        "years_at_current_address",
        "bank_balance_at_application",
    ]


def test_load_experiment_data_returns_expected_shapes_and_target():
    X, y = load_experiment_data()

    assert len(X) == 50_000
    assert X.shape[1] == 5
    assert len(y) == len(X)
    assert list(X.columns) == FEATURES
    assert y.name == "default"
    assert not X.isna().any().any()
    assert not y.isna().any()


def test_target_is_boolean_and_contains_both_classes():
    _, y = load_experiment_data()

    assert pd.api.types.is_bool_dtype(y)
    assert set(y.unique()) == {False, True}


def test_loaded_features_exclude_identifiers_and_target():
    X, _ = load_experiment_data()

    forbidden_columns = {"cust_id", "loan_id", "default"}

    assert forbidden_columns.isdisjoint(X.columns)


def test_loader_rejects_missing_approved_feature(monkeypatch):
    import src.baseline_experiment as experiment

    original_read_csv = pd.read_csv

    def fake_read_csv(path, *args, **kwargs):
        frame = original_read_csv(path, *args, **kwargs)

        if str(path).endswith("customers.csv"):
            return frame.drop(columns=["income"])

        return frame

    monkeypatch.setattr(pd, "read_csv", fake_read_csv)

    with pytest.raises((ValueError, KeyError)):
        experiment.load_experiment_data()
