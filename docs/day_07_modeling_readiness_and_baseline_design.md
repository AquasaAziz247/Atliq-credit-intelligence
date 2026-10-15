# Day 7: Modeling Readiness and Baseline Design

## 1. Objective

Close the bounded investigation of target provenance, consolidate feature-timing and leakage decisions, select a modeling-readiness outcome, and design a conditional educational baseline.

This is an independent educational portfolio prototype, not a validated lending-risk system.

## 2. Executive decision

**Outcome B: A limited educational classification experiment may be considered later, with explicit assumptions and restricted claims.**

The supplied `default` column is structurally valid as a binary label, but its business definition, generation process, observation window, assignment date, and maturity remain unverified. No feature is certified as point-in-time safe.

This decision permits consideration of an experiment that learns to classify the supplied labels for educational purposes. It does not establish that the labels represent future defaults or that the resulting model would be suitable for a real lending workflow.

If a defensible real-world future-default prediction claim is required, use Outcome C and keep model training blocked until critical target-provenance and feature-timing gaps are resolved.

**No model was trained during Day 7. No raw data was changed.**

## 3. Evidence reviewed

The investigation reviewed:

- `README.md`
- `reports/data_audit.txt`
- `docs/day_03_decision_log.md`
- `docs/day_04_relationship_target_audit.md`
- `docs/day_05_data_contracts_and_readiness.md`
- `docs/day_06_target_and_feature_timing_review.md`
- Notebook metadata and introductory Markdown in the available notebooks
- CSV schemas and existing validation results

No authoritative target definition, target-generation process, observation window, label-assignment date, or feature-timestamp documentation was found in the inspected local project materials. This does not prove that the original dataset provider has no such documentation.

## 4. Verified facts

- `customers.csv`: 50,000 rows and 12 columns.
- `loans.csv`: 50,000 rows and 15 columns.
- `bureau_data.csv`: 50,000 rows and 8 columns.
- The configured structural contracts passed in the previous validation run.
- All 50,000 loan customer IDs matched customer and bureau customer IDs.
- Both validated left joins preserved 50,000 rows, with zero unmatched records.
- `default` is complete and Boolean.
- `default = False`: 45,703 records.
- `default = True`: 4,297 records.
- Supplied positive-label proportion: 8.594%.
- `residence_type` has 62 missing values.
- Eight records have `loan_amount = 0` and `principal_outstanding = -1`; all eight have `default = False`.
- Seven records have `processing_fee > loan_amount`.
- `principal_outstanding` equals 5,000,000 in 1,840 records.
- All 50,000 `net_disbursement` values match 80% of `loan_amount` within 0.01.
- The bureau schema contains no snapshot-date column.
- All audited installment start dates occur after their recorded disbursal dates.
- The last recorded test run reported 31 passing tests. Tests and validation must be rerun after this report is created.

These observations establish structural properties and dataset patterns. They do not establish the target's business meaning, temporal validity, or a real banking rule.

## 5. Target provenance: facts, assumptions, and unknowns

### Verified

- A complete Boolean column named `default` exists in `loans.csv`.
- It contains 4,297 positive labels and 45,703 negative labels.
- The project documentation and available notebook introductions identify the target-generation process and observation horizon as undocumented.

### Working assumption

The proposed prediction point is before loan approval or disbursement. This is a project assumption, not a verified property of the source data.

### Unresolved questions

1. What business event does `default = True` represent?
2. Does the label describe an existing state or a future event?
3. What event or threshold creates a positive label?
4. What is the outcome observation window and prediction horizon?
5. When was each label assigned?
6. Have negative labels had sufficient follow-up time?
7. How are active, immature, or censored loans handled?
8. Was the label generated using any supplied feature or later account state?

## 6. Feature availability and leakage matrix

The following classifications are provisional. A plausible column name does not prove that the value was available at the proposed prediction point.

| Feature group or fields | Day 7 decision | Evidence needed |
|---|---|---|
| `age` | Candidate, unverified | Application snapshot and age reference date |
| `gender` | Candidate, unverified | Definition, timing, and appropriate-use review |
| `marital_status` | Candidate, unverified | Application snapshot |
| `employment_status` | Candidate, unverified | Application snapshot and category definition |
| `income` | Candidate, unverified | Units, income period, and reference date |
| `number_of_dependants` | Candidate, unverified | Definition and reference date |
| `residence_type` | Candidate, unverified | Definition, timestamp, and missingness policy |
| `years_at_current_address` | Candidate, unverified | Calculation method and reference date |
| `loan_purpose`, `loan_type` | Candidate, unverified | Application schema and decision workflow |
| `bank_balance_at_application` | Candidate, unverified | Measurement method and timestamp |
| `sanction_amount`, `loan_amount`, `loan_tenure_months` | Unresolved | Requested versus approved meaning and timestamp |
| `city`, `state`, `zipcode` | Unresolved | Timing, usefulness, privacy, and generalization review |
| Bureau account counts, loan months, delinquency, DPD, enquiries, utilization | Unresolved, high scrutiny | Definitions, snapshot date, and measurement windows |
| `principal_outstanding` | Exclude initially | May reflect a later account state |
| `processing_fee`, `gst`, `net_disbursement` | Exclude initially | May be determined during or after the lending decision |
| `disbursal_date`, `installment_start_dt` | Exclude from initial predictors | Event timing and validation design require review |
| `cust_id`, `loan_id` | Never ordinary predictors | Retain for joins and audit trails only |
| `default` | Label only | Must never be included as an input feature |

No feature is certified as point-in-time safe. Reconsideration requires supporting evidence of its definition and availability at the chosen prediction timestamp.

## 7. Data-quality handling

| Finding | Current policy |
|---|---|
| 62 missing `residence_type` values | Preserve; select a justified preprocessing policy later |
| Eight zero-loan records with `principal_outstanding = -1` | Flag and investigate; do not silently delete or recode |
| Seven processing-fee anomalies | Preserve and investigate definitions and units |
| 1,840 repeated maximum outstanding values | Preserve; do not assume capping without evidence |
| Net-disbursement values matching 80% of loan amount | Record as an observed relationship, not a verified business rule |
| Missing bureau snapshot date | Keep bureau features out of the initial feature set pending timing evidence |

No automatic deletion, capping, imputation, or rewriting of raw records is authorized by these observations.

## 8. Conditional baseline design

This section specifies a future experiment; it does not authorize or report training results.

### 8.1 Unit of analysis and label

Use one loan record per row, reflecting the supplied table structure. Treat `default` as an undocumented supplied label. Do not describe it as verified future default.

### 8.2 Initial feature policy

If the educational experiment proceeds, begin with a conservative set of candidate customer and application attributes whose meanings and timing are explicitly marked unverified.

Exclude:
- `default` from predictors
- `cust_id` and `loan_id`
- `principal_outstanding`
- `processing_fee`, `gst`, and `net_disbursement`
- Bureau features until their snapshot timing and definitions are supported
- Other fields whose timing or meaning cannot be justified for the stated experiment

This is a provisional experiment policy, not a declaration that any included feature has been proven safe for real-world lending decisions.

### 8.3 Preprocessing

- Keep raw CSV files unchanged.
- Use a reproducible scikit-learn pipeline for learned preprocessing.
- Handle missing categorical values explicitly.
- Fit imputers, encoders, scalers, and feature-selection steps on training data only.
- Apply the fitted transformations to validation and test data without refitting.
- Preserve and document anomaly flags rather than silently removing records.
- Add tests for transformations and train/test isolation before relying on the pipeline.

### 8.4 Validation strategy

The validation design must match the limited educational question being asked.

- A stratified random split may be considered for a basic educational classification experiment, with its limitations documented.
- A chronological split should only be used if the available dates and intended evaluation setting justify it.
- The existing disbursal dates do not establish the target observation window or label maturity.
- Neither a random nor a chronological split repairs unknown target semantics or unverified feature timing.
- Keep the test set isolated until final evaluation.

### 8.5 Models and evaluation

If the experiment is later approved, compare:

1. A majority-class dummy classifier as a simple baseline.
2. Logistic regression in a preprocessing pipeline as an interpretable candidate model.

Evaluate using precision, recall, F1, PR-AUC, ROC-AUC, and a confusion matrix where the evaluation setup supports them. Do not rely on accuracy alone. Document class imbalance, threshold assumptions, and uncertainty.

Do not report performance numbers until the corresponding experiment has actually been run and its outputs reviewed.

### 8.6 Leakage controls

- Never include the target or identifiers in ordinary predictors.
- Keep high-risk process and account-state fields excluded initially.
- Require evidence before reconsidering bureau fields.
- Fit learned preprocessing only on training data.
- Document the exact feature list and split strategy.
- Clearly distinguish label-reproduction performance from validated future-default prediction.

## 9. Readiness decision and conditions

**Selected outcome: B, limited educational classification under explicit assumptions.**

Reasons:
- The supplied binary label is structurally valid.
- Dataset relationships and basic validation checks pass.
- The project can teach reproducible preprocessing, baseline comparison, and evaluation.
- The business definition and temporal meaning of the label remain unknown.
- No feature is certified as available at the proposed prediction point.

Before any experiment:
1. Seek authoritative target definition and generation logic.
2. Seek the observation window, label-assignment date, and evidence of label maturity.
3. Define the intended prediction point.
4. Obtain feature definitions and timestamps, especially for bureau fields.
5. Document anomalies and justified treatment without changing raw source files.
6. Finalize the feature list and validation design for the limited experiment.
7. Disclose remaining assumptions in the README and experiment report.

If the project is expected to demonstrate a defensible real-world future-default model, change the decision to Outcome C and keep training blocked until the critical provenance gaps are resolved.

## 10. Day 8 recommendation

Prioritize a reproducible baseline implementation plan and tests only after reviewing this report. Before training on the supplied label, revisit whether the educational experiment is worth proceeding with given the unresolved target semantics. Continue seeking authoritative data documentation if available.

Do not add model-performance claims, change raw data, or describe the prototype as a validated lending system.

## 11. Interview preparation

**Why is a valid binary target not necessarily a valid prediction target?**

A column can be complete and correctly typed while its business definition, event timing, observation window, and maturity remain unknown.

**Why can a bureau join still leak information?**

Matching identifiers establish relationship integrity, not that the bureau snapshot predates the prediction timestamp.

**Why is a dummy classifier useful?**

It provides a simple reference point for judging whether a candidate model adds value beyond a basic prediction strategy.

**Why fit preprocessing only on training data?**

Fitting learned transformations on the full dataset can expose the training process to information from held-out data and produce an overly optimistic evaluation.

**Why not rely on accuracy alone?**

With an imbalanced target, accuracy can hide poor identification of the minority class. Precision, recall, PR-AUC, and a confusion matrix provide additional information.

**What does Outcome B permit?**

A clearly labelled educational experiment on the supplied labels, not a claim that future-default prediction has been validated for real lending decisions.

## 12. Day 7 completion checklist

- [x] Inspect existing project documentation and target-related decisions.
- [x] Review CSV schemas and target counts.
- [x] Search inspected local materials for authoritative target and timing documentation.
- [x] Consolidate provisional feature availability and leakage decisions.
- [x] Select a modeling-readiness outcome and specify a conditional baseline design.
- [ ] Review this report and its Git diff.
- [ ] Re-run tests and validation.
- [ ] Review Git status and preserve unrelated changes.
- [ ] Commit only this reviewed Day 7 report, after explicit review.

No model has been trained. No raw data has been changed.

## 13. Codebasics Reference Notebook Review

### 13.1 Purpose and scope

The original Codebasics credit-risk modeling notebook was reviewed as a methodological reference. It is not authoritative documentation of this project's target-generation process or feature timestamps.

### 13.2 Workflow observed

The reference covers data preparation, exploratory analysis, feature engineering, feature selection, encoding, logistic regression, Random Forest, XGBoost, class-imbalance handling, and evaluation. It explores loan-to-income, delinquency, and average DPD per delinquency as engineered features. These are ideas to assess, not automatically approved predictors.

### 13.3 Reported result

The reference notebook reports an AUC of 0.98. This is a result reported by that notebook, not independently reproduced for this project. It does not establish valid future-default prediction on this dataset.

### 13.4 Practices worth evaluating

- Compare models with a simple dummy baseline.
- Use reproducible splits appropriate to the experiment.
- Fit learned preprocessing transformations on training data only.
- Evaluate imbalanced classification with metrics beyond accuracy.
- Document feature engineering, selection, and evaluation decisions.

### 13.5 Practices not to copy blindly

- Exclude bureau delinquency, DPD, and credit-utilization features until their timing, definitions, and measurement windows are supported.
- Treat engineered features derived from unverified fields as carrying the same timing risks.
- Do not copy the reference notebook's AUC into this project's results.
- Do not treat high AUC as proof that target semantics, label maturity, or temporal leakage concerns are resolved.

### 13.6 Decision

Use the Codebasics notebook as a learning and methodology reference. Preserve this project's data contracts, anomaly-handling policy, feature-timing review, and explicit limitations. Adapt only practices that can be justified and tested.

The reference does not resolve the provenance gaps identified in this review. No model was trained as part of this Day 7 review.
