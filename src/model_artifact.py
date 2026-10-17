"""Local serialization workflow for the educational AtliQ inference model.

The saved pipeline is an artifact of the existing baseline training process.
Serialization changes deployment mechanics, not model performance or validity.
Only load artifacts generated from a trusted local project environment.
"""

from pathlib import Path

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.baseline_experiment import RAW_DATA
from src.model_inference import train_inference_model

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ARTIFACT_PATH = PROJECT_ROOT / "models" / "baseline_inference_pipeline.joblib"
REQUIRED_RAW_FILES = (RAW_DATA / "customers.csv", RAW_DATA / "loans.csv")


def validate_model_pipeline(model: object) -> Pipeline:
    """Validate that an artifact is the expected fitted sklearn pipeline."""
    if not isinstance(model, Pipeline):
        raise ValueError("Model artifact must contain a scikit-learn Pipeline.")

    if list(model.named_steps) != ["scaler", "classifier"]:
        raise ValueError(
            "Model artifact must contain exactly the 'scaler' and 'classifier' steps."
        )

    if not isinstance(model.named_steps["scaler"], StandardScaler):
        raise ValueError("Model artifact 'scaler' step must be StandardScaler.")

    classifier = model.named_steps["classifier"]
    if not isinstance(classifier, LogisticRegression):
        raise ValueError(
            "Model artifact 'classifier' step must be LogisticRegression."
        )

    if not hasattr(classifier, "classes_"):
        raise ValueError("Model artifact classifier must be fitted before saving/loading.")

    if True not in list(classifier.classes_):
        raise ValueError("Model artifact classifier must include the True positive class.")

    return model


def generate_model_artifact(
    artifact_path: str | Path = DEFAULT_ARTIFACT_PATH,
) -> Path:
    """Train via the established inference function and save the fitted pipeline."""
    missing = [path for path in REQUIRED_RAW_FILES if not path.is_file()]
    if missing:
        expected = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(
            "Cannot generate the local model artifact because required source CSV "
            f"file(s) are missing: {expected}. Place customers.csv and loans.csv "
            "in data/raw/ and rerun: python -m src.model_artifact"
        )

    model = validate_model_pipeline(train_inference_model())
    destination = Path(artifact_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, destination)
    return destination


def load_model_artifact(
    artifact_path: str | Path = DEFAULT_ARTIFACT_PATH,
) -> Pipeline:
    """Load and validate a trusted locally generated model artifact."""
    source = Path(artifact_path)
    if not source.is_file():
        raise FileNotFoundError(
            f"Model artifact not found: {source}. Generate it locally after placing "
            "customers.csv and loans.csv in data/raw/ by running "
            "'python -m src.model_artifact'. The generated models/ artifact is "
            "intentionally excluded from Git and must be created in each environment."
        )

    try:
        model = joblib.load(source)
    except Exception as exc:
        raise ValueError(
            f"Could not load model artifact at {source}. Regenerate it with "
            "'python -m src.model_artifact'."
        ) from exc

    return validate_model_pipeline(model)


def main() -> int:
    """CLI entry point for creating the local artifact."""
    try:
        destination = generate_model_artifact()
    except (FileNotFoundError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"Model artifact generated: {destination}")
    print("Educational label-classification artifact only; not validated for lending.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
