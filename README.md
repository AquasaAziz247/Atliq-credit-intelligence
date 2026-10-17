# AtliQ Credit Intelligence

**An educational credit-risk classification and ML engineering project**

[**Live Demo**](https://atliq-credit-intelligence.streamlit.app/) · [**GitHub Repository**](https://github.com/AquasaAziz247/Atliq-credit-intelligence)

> **Important:** This is an educational prototype. Its model outputs are not validated estimates of future loan default, and its scorecard must not be used for real lending decisions.

## Overview

AtliQ Credit Intelligence explores the development of a reproducible machine-learning workflow for a supplied-label credit-classification task.

The project focuses on data quality, relational validation, exploratory data analysis, leakage-aware experiment design, baseline modeling, model evaluation, automated testing, model serialization, and interactive deployment.

The objective is to demonstrate practical ML engineering skills while documenting the limitations that prevent the current model from being interpreted as a validated future-default prediction system.

## Live application

The Streamlit application accepts five numerical inputs and displays:

- An experimental positive-class probability
- An illustrative score out of 900
- A score category
- An explanation of the score and its limitations

The application loads a saved scikit-learn pipeline through a joblib artifact.

**The displayed probability is not a validated future-default probability.** The score is a custom mathematical transformation, not a calibrated or industry-standard credit score.

## Technology stack

- **Language:** Python
- **Data analysis:** pandas, NumPy
- **Machine learning:** scikit-learn, Logistic Regression, StandardScaler
- **Visualization:** Plotly
- **Application:** Streamlit
- **Model serialization:** joblib
- **Testing:** pytest
- **Version control:** Git and GitHub
- **Deployment:** Streamlit Community Cloud

## Architecture

```text
Educational source datasets
          |
          v
Data auditing and validation
          |
          v
EDA and feature/timing review
          |
          v
Leakage-aware experiment design
          |
          v
StandardScaler + Logistic Regression
          |
          v
Saved model artifact (.joblib)
          |
          v
Streamlit input interface
          |
          v
Experimental probability and illustrative score
```

The model artifact separates training from prediction-time inference. Regenerating the artifact requires the original source CSV files locally; the deployed app uses the saved artifact for predictions.

## Dataset and data-quality analysis

The educational dataset contains three CSV files, each with 50,000 records:

| Dataset | Records | Purpose |
|---|---:|---|
| `customers.csv` | 50,000 | Customer attributes |
| `loans.csv` | 50,000 | Loan records and supplied target |
| `bureau_data.csv` | 50,000 | Credit bureau information |

The supplied `default` label contains:

- **45,703** records labeled `False`
- **4,297** records labeled `True`
- **8.594%** positive-label proportion

The initial audit identified several patterns requiring investigation:

- 62 missing `residence_type` values
- 8 records with zero loan amounts and `principal_outstanding = -1`
- 7 records where `processing_fee` exceeds a positive `loan_amount`
- 1,840 records with `principal_outstanding = 5,000,000`
- An observed relationship in which `net_disbursement` matches approximately 80% of `loan_amount` across the reviewed records

These findings are observations, not proof that the records are erroneous or that the observed formula represents a genuine banking rule.

The project also includes relationship checks, join validation, data contracts, preprocessing tests, and explicit documentation of unresolved data questions.

**Data handling:** The raw CSV files are excluded from version control. They are not distributed with the repository and must be available locally for data-dependent experiments and artifact generation.

## Baseline machine-learning workflow

The baseline pipeline uses:

1. `StandardScaler` for feature scaling
2. `LogisticRegression` for binary classification

The five baseline features are:

- `age`
- `income`
- `number_of_dependants`
- `years_at_current_address`
- `bank_balance_at_application`

The established stratified data split uses random seed 42:

| Partition | Records | Purpose |
|---|---:|---|
| Fit | 32,000 | Fit the model |
| Validation | 8,000 | Evaluate and compare experiments |
| Reserved test | 10,000 | Hold out for final evaluation |

The reserved test partition is not intended for repeated model selection or threshold tuning.

The project compares the baseline with a class-weighted Logistic Regression experiment and documents the effect of the decision threshold on precision and recall.

### Recorded validation results

The baseline achieved a validation ROC-AUC of approximately **0.5817**. The class-weighted experiment achieved approximately **0.5815**.

At the baseline decision threshold of 0.075, the recorded validation metrics were:

| Metric | Result |
|---|---:|
| Precision | 9.94% |
| Recall | 76.89% |
| F1-score | 0.1761 |

The low precision and modest ROC-AUC indicate limited discriminative performance. The threshold also produces many positive predictions.

These results are presented as experimental findings, not as evidence that the model satisfies real-world credit-risk requirements.

## Educational scorecard

The application transforms the experimental positive-class probability \(p\) into an illustrative score:

\[
S=\operatorname{round}(900-600p)
\]

The configured score categories are:

| Score | Category |
|---|---|
| 750–900 | Excellent |
| 650–749 | Good |
| 500–649 | Average |
| 300–499 | Poor |

This scorecard is a custom demonstration of translating a model output into a user interface. It is not calibrated, validated, or intended to represent an industry-standard credit score.

## Testing and verification

The latest reported full test run in the development environment completed successfully:

```text
84 passed in 4.49s
```

The automated tests cover data contracts, relationship validation, preprocessing, baseline experiments, class weighting, model inference, artifact handling, and scorecard behavior.

The live application was also manually checked for successful rendering, prediction output, visible limitations, and prediction after a browser refresh.

These checks establish useful functional evidence for the current prototype. They do not establish production readiness, model validity for lending, or complete post-deployment regression coverage.

## Run locally

### 1. Clone the repository

```powershell
git clone https://github.com/AquasaAziz247/Atliq-credit-intelligence.git
cd Atliq-credit-intelligence
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Use a Python version compatible with the pinned dependencies.

### 3. Add the source data locally

Place the required original files in `data/raw/`:

```text
data/raw/
├── customers.csv
├── loans.csv
└── bureau_data.csv
```

The CSV files are not included in the public repository.

### 4. Generate the model artifact

```powershell
python -m src.model_artifact
```

This uses the established training workflow and saves the pipeline to:

```text
models/baseline_inference_pipeline.joblib
```

### 5. Launch the application

```powershell
python -m streamlit run app.py
```

### 6. Run the tests

```powershell
python -m pytest -v
```

Artifact generation requires the local source datasets. Once a compatible artifact exists, prediction-time inference uses that artifact rather than retraining from the CSV files on each submission.

Only load trusted joblib artifacts because Python object deserialization can execute code.

## Key limitations

Several questions remain unresolved:

- The target-generation process and the meaning of the supplied `default` label are not sufficiently documented.
- The outcome horizon and label-maturity rules are unknown.
- Feature collection timestamps and point-in-time eligibility have not been established for every candidate feature.
- The baseline's predictive performance is weak.
- The probability has not been validated or calibrated as a future-default estimate.
- The illustrative scorecard has not been validated for real lending.
- The project does not establish fairness, suitability for individual credit decisions, or production readiness.

These limitations constrain the conclusions that can be drawn from the current experiments. Resolving target provenance and feature timing is a prerequisite for making defensible claims about future-default prediction.

## Future work

Potential next steps include:

1. Investigate target construction, observation windows, and label maturity.
2. Verify feature definitions and prediction-time availability.
3. Improve validation design once the target and timing assumptions are supported.
4. Conduct further candidate-model experiments using training and validation data.
5. Evaluate precision-recall trade-offs, calibration, and threshold behavior where methodologically appropriate.
6. Expand integration and post-deployment regression testing.
7. Improve interpretability and document responsible-use considerations.

Any future model comparison should preserve the reserved test partition until the final evaluation is justified.

## Project links

- **Live application:** https://atliq-credit-intelligence.streamlit.app/
- **Source code:** https://github.com/AquasaAziz247/Atliq-credit-intelligence

*AtliQ Credit Intelligence is an independent educational portfolio prototype. It is not a real bank product, and it must not be used to make actual lending decisions.*
