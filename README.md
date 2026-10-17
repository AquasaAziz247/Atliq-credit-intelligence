# AtliQ Credit Intelligence

An educational credit-risk analytics and machine-learning portfolio project focused on data quality, exploratory analysis, leakage prevention, baseline classification, and an initial Streamlit inference prototype.

> **Project status:** Data auditing, exploratory data analysis, data-contract validation, baseline classification experiments, and a class-weighting comparison are complete. A reusable inference module and Streamlit prototype have been added. Target semantics, feature collection timing, and the validity of future-default prediction remain unresolved. The project is educational and is not a validated lending or credit-scoring system.

## Objectives

- Audit customer, loan, and bureau datasets.
- Explore loan and supplied default-label patterns.
- Document suspicious records and unresolved data-quality questions.
- Assess whether candidate features could be available at the proposed prediction point.
- Develop reproducible, tested data-validation and inference utilities.
- Compare baseline classification experiments without overstating their results.
- Provide an interactive interface for exploring experimental model outputs.

## Technology

- Python 3.13
- pandas
- NumPy
- scikit-learn
- Plotly
- pytest
- Streamlit
- Git

## Project structure

```text
atliq-credit-intelligence/
├── data/
│   └── raw/                 # Local source CSV files; not committed
├── docs/                    # Day-by-day decisions, evidence and limitations
├── notebooks/
│   ├── day_02_eda.ipynb
│   └── day_03_feature_engineering_leakage_audit.ipynb
├── reports/
│   ├── data_audit.txt
│   └── day_10_class_weighting_results.txt
├── src/
│   ├── audit_data.py
│   ├── baseline_experiment.py
│   ├── class_weighting_experiment.py
│   ├── contract_validation.py
│   ├── data_contracts.py
│   ├── eda.py
│   ├── model_inference.py
│   ├── preprocessing.py
│   └── ...
├── tests/
│   ├── test_baseline_experiment.py
│   ├── test_class_weighting_experiment.py
│   ├── test_contract_validation.py
│   ├── test_model_inference.py
│   ├── test_preprocessing.py
│   └── ...
├── app.py
├── requirements.txt
└── README.md
```

The ellipses indicate additional existing source files, tests, and documentation. This is a representative structure, not an exhaustive file listing.

## Local setup

Use Python 3.13 or another Python version compatible with the pinned dependencies.

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The raw CSV files are not included in version control. Place the expected files in `data/raw/` before running scripts that require the source datasets.

## Run the data audit

```powershell
python src/audit_data.py
```

## Run tests

```powershell
python -m pytest -v
```

The full test suite passed **50 tests** during the Day 12 clean-environment verification.

## Run the Streamlit prototype

From the project root, with the virtual environment activated, ensure `data/raw/customers.csv` and `data/raw/loans.csv` exist locally. Generate the baseline inference artifact first:

```powershell
python -m src.model_artifact
```

Then launch the application:

```powershell
python -m streamlit run app.py
```

The artifact is saved to `models/baseline_inference_pipeline.joblib`, which is excluded from version control. Generate it separately in each environment. The app loads this saved pipeline for predictions and does not need the raw CSV files at prediction time. Only load trusted artifacts.

The application accepts five baseline features and displays an experimental positive-class probability. The pipeline is fitted through the established training function using the existing fit partition.

**Important:** The displayed value is not a validated or calibrated estimate of future loan default. It must not be used to approve or reject a loan.

## Data findings

The supplied dataset contains 50,000 customer records, 50,000 loan records, and 50,000 bureau records.

The loan table contains 4,297 records labeled `default = True`, representing 8.594% of the supplied labels.

Initial investigations identified:

- 62 missing `residence_type` values.
- 8 records with zero loan amounts and `principal_outstanding = -1`.
- 7 records where `processing_fee` exceeds a positive `loan_amount`.
- 1,840 records where `principal_outstanding` equals 5,000,000.
- An observed relationship in which all 50,000 `net_disbursement` values match 80% of `loan_amount` within 0.01.

These are observations, not proof that the flagged records are erroneous or that the observed formula represents a real banking rule.

## Modeling and validation

The project includes baseline logistic-regression experiments, a class-weighting comparison, and a reusable inference path.

The current baseline uses these five features:

- `age`
- `income`
- `number_of_dependants`
- `years_at_current_address`
- `bank_balance_at_application`

The inference function fits the model on the established fit partition rather than the validation or reserved test partitions. The current application does not perform new feature engineering, threshold tuning, or model selection.

The project has not demonstrated that the original assignment's precision and recall requirements have been satisfied. Model outputs and experimental metrics should be interpreted in the context of the documented data and evaluation limitations.

## Important limitations

The dataset's target-generation logic, default observation horizon, label maturity, and feature timestamps are undocumented. Although the proposed prediction point is before loan approval or disbursement, feature eligibility has not been verified.

The supplied `default` label has not been established as a reliable future-default outcome for a defined prediction horizon. A positive-class probability therefore must not be presented as a validated future-default probability.

Fields that may reflect post-decision or later account information will not be treated as valid predictors without supporting evidence.

This project is an educational portfolio prototype, not a validated lending system. It is not intended for real credit decisions.

## Project documentation

The `docs/` directory contains the project's day-by-day decisions, data-readiness reviews, modeling experiments, requirements, evidence, and prototype limitations. Consult those documents for the detailed reasoning and experiment-specific results.

See also: [Day 13: Educational Scorecard Integration](docs/day_13_scorecard.md).
