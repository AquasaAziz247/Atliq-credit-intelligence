# Day 11: Requirements and Evidence Matrix

## 1. Purpose

Record the original assignment requirements, current dataset evidence, unresolved assumptions, and prerequisites for further modelling.

This document describes an educational portfolio prototype. It does not establish that the supplied dataset supports validated future-default prediction.

## 2. Original assignment requirements

| Requirement                              | Evidence                                                            | Status                                  | Next action                                          |
| ---------------------------------------- | ------------------------------------------------------------------- | --------------------------------------- | ---------------------------------------------------- |
| Estimate default probability             | `loans.default` exists, but its business definition is undocumented | Unresolved                              | Investigate target semantics and observation horizon |
| Produce a score from 300 to 900          | Original assignment specifies the range                             | Mapping undefined                       | Define and validate a transparent conversion         |
| Use Poor, Average, Good, Excellent bands | Assignment supplies the four bands                                  | Bands known; boundaries need definition | Specify exact endpoint handling                      |
| Default-class recall above 90%           | Existing experiments have not demonstrated this                     | Not achieved                            | Evaluate on validation data                          |
| Default-class precision above 50%        | Existing experiments have not demonstrated this                     | Not achieved                            | Investigate the precision-recall trade-off           |
| Explainable business rules               | Logistic Regression experiments exist                               | Incomplete                              | Review coefficients and interpretation limits        |
| Human review for false positives         | Mentioned in the assignment                                         | Design pending                          | Define a review process if justified                 |

### Assigned score bands

- 300–500: Poor
- 500–650: Average
- 650–750: Good
- 750–900: Excellent

The assignment does not specify the probability-to-score formula or how shared band endpoints should be assigned. These must be documented before implementation.

## 3. Dataset evidence

The local datasets contain 50,000 records each:

- `customers.csv`: 12 columns.
- `loans.csv`: 15 columns.
- `bureau_data.csv`: 8 columns.

The observed `default` label contains 45,703 False and 4,297 True records, giving an 8.594% positive-label rate.

Existing audits report complete customer-join coverage. These structural findings do not establish target meaning or point-in-time feature validity.

The bureau schema does not contain an identified snapshot-date column. The bureau fields' collection date and measurement windows remain unresolved.

## 4. Feature evidence and proposed policy

| Feature or group                                                                                   | Current evidence                                                             | Proposed policy                                                            |
| -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `age`, `income`, `number_of_dependants`, `years_at_current_address`, `bank_balance_at_application` | Used in existing baseline experiments; collection timestamps are unverified  | Retain for educational baseline comparisons with an explicit timing caveat |
| `number_of_open_accounts`, `number_of_closed_accounts`, `credit_utilization_ratio`                 | Present in the bureau schema and mentioned in the assignment                 | Verify definitions and snapshot timing before adding                       |
| `total_dpd`, `delinquent_months`, `total_loan_months`, `enquiry_count`                             | Present in the bureau schema; measurement windows are unknown                | Verify definitions and timing before adding                                |
| `loan_amount` and `income`                                                                         | Both fields exist; income period and loan amount semantics need confirmation | Candidate for a loan-to-income ratio                                       |
| `delinquent_months` and `total_loan_months`                                                        | Both fields exist; compatible measurement periods are unverified             | Candidate for a delinquency ratio                                          |
| `total_dpd` and `delinquent_months`                                                                | Both fields exist; definitions and measurement periods are unverified        | Candidate for average DPD per delinquent month                             |
| `principal_outstanding`                                                                            | May reflect later account-state information                                  | Continue excluding from the initial feature set                            |
| `processing_fee`, `gst`, `net_disbursement`                                                        | Timing relative to the lending decision is unresolved                        | Continue excluding from the initial feature set                            |
| `sanction_amount`, `loan_tenure_months`                                                            | Lending-process fields with unresolved timing                                | Defer until availability is established                                    |
| Geographic fields                                                                                  | Present, but usefulness and generalization have not been assessed            | Defer to a separate review                                                 |

The original assignment clarifies the intended use of bureau information but does not prove that the supplied bureau values were available at the intended prediction point.

## 5. Proposed ratio definitions and safeguards

### 5.1 Loan-to-income ratio

Candidate formula:

`loan_amount / income`

Before implementation:

- Confirm the period and units represented by `income`.
- Confirm the business meaning of `loan_amount`.
- Treat missing or zero income as requiring explicit handling, not as an automatic zero ratio.
- Investigate negative or otherwise invalid source values.
- Document whether affected rows are flagged, treated as missing, or excluded from a specific analysis.

### 5.2 Delinquent-months ratio

Candidate formula:

`delinquent_months / total_loan_months`

Before implementation:

- Confirm both fields use compatible measurement windows.
- A zero denominator makes the ratio undefined.
- Investigate negative values and delinquent months greater than total loan months.
- Document handling of missing and inconsistent values.

### 5.3 Average DPD per delinquent month

Candidate formula:

`total_dpd / delinquent_months`

Before implementation:

- Confirm the meaning and units of `total_dpd`.
- A zero denominator makes the ratio undefined, not automatically zero.
- Investigate negative or inconsistent values.
- Document handling of missing values and invalid records.

No imputation or exclusion policy is approved by this document. Each policy requires evidence, justification, and tests before implementation.

## 6. Target and timing limitations

The following remain unresolved:

- Business definition of `default`.
- Target observation horizon and label-assignment timing.
- Whether negative labels have sufficiently matured.
- Actual collection timestamps for the current five model features.
- Bureau snapshot dates and measurement windows.
- Whether the intended prediction point is before approval or disbursement.

The proposed pre-approval or pre-disbursement prediction point remains an assumption, not a verified fact.

Until critical target and timing evidence is available, results must be described as educational classification experiments on the supplied labels, not as a validated future-default prediction model.

## 7. Existing modelling evidence

The baseline Logistic Regression and class-weighting experiments have been completed.

The recorded validation ROC-AUC was approximately 0.5817 for the baseline and 0.5815 for the balanced-class experiment. The existing experiments have not demonstrated that default-class recall above 90% and precision above 50% can be achieved together.

The Day 8 baseline did evaluate its test split, as documented in the earlier experiment records. The Day 10 class-weighting comparison used validation data and did not evaluate its reserved test partition.

Do not use the reserved test partition for further feature selection, threshold tuning, or model comparison.

## 8. Probability-to-score and explainability plan

Before implementing a score:

1. Clarify target semantics and the prediction setting.
2. Evaluate model discrimination and probability calibration using appropriate validation data.
3. Define a transparent probability-to-score mapping without presenting it as an official banking formula.
4. Specify exact score-band boundaries.
5. Test the score range, monotonicity, reproducibility, and edge cases.
6. Review model coefficients and their interpretation limits before translating them into proposed business rules.

The assignment's score bands alone do not validate a creditworthiness interpretation.

## 9. Data integrity and change-control policy

- Preserve raw CSV files unchanged.
- Do not silently remove suspicious records.
- Keep verified facts distinct from hypotheses and assumptions.
- Fit learned preprocessing transformations on training data only.
- Add tests for every approved transformation.
- Preserve unrelated working-tree changes.
- Do not stage or commit changes until the diffs have been reviewed and explicitly approved.

## 10. Next actions

1. Review this requirements-and-evidence matrix.
2. Investigate any available authoritative target and feature-timing documentation.
3. Decide which ratio definitions can be justified.
4. Implement approved feature transformations with tests.
5. Correct the README to reflect completed experiments and outstanding limitations.
6. Reassess model performance and score mapping only after the necessary definitions and validation design are established.
