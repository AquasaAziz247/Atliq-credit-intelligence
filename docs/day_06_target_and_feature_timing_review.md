# Day 6: Target Provenance and Feature-Timing Review

## 1. Objective

Review available project evidence about the `default` target, assess feature-timing and leakage risks, revisit data-quality findings, and decide whether an educational modelling experiment is justified.

This is an independent educational portfolio prototype, not a validated lending-risk system.

## 2. Executive decision

**Outcome B: A limited educational classification experiment may be considered later, with explicit assumptions and restricted claims.**

The target is structurally valid, but its business definition, generation logic, observation window, prediction horizon, and label maturity remain undocumented. Current evidence does not establish that `default` represents a future default observed over a defined period.

No model was trained during this review.

If the project requires a defensible real-world future-default prediction claim, obtain authoritative target and feature-lineage documentation before modelling.

## 3. Evidence reviewed

- `README.md`
- `docs/day_03_decision_log.md`
- `docs/day_04_relationship_target_audit.md`
- `docs/day_05_data_contracts_and_readiness.md`
- `reports/data_audit.txt`
- `src/day4_target_check.py`
- `src/day4_feature_timing_check.py`
- `notebooks/day_03_feature_engineering_leakage_audit.ipynb`
- CSV schemas and a fresh read-only quality check

No authoritative target definition, target-generation process, observation window, or feature timestamp documentation was found in the inspected local materials. This does not prove that documentation is unavailable from the original data provider.

## 4. Verified facts

- Customers: 50,000 rows, 12 columns.
- Loans: 50,000 rows, 15 columns.
- Bureau: 50,000 rows, 8 columns.
- Configured Day 5 structural contracts pass.
- All loan customer IDs match records in customer and bureau tables.
- Both validated left joins preserve 50,000 rows, with zero unmatched records.
- `default` is complete and Boolean.
- `default = False`: 45,703 records.
- `default = True`: 4,297 records.
- Positive-label proportion: 8.594%.
- `residence_type` has 62 missing values.
- Eight records have `loan_amount = 0` and `principal_outstanding = -1`.
- All eight zero-loan records have `default = False`.
- Seven records have `processing_fee > loan_amount`.
- `principal_outstanding` equals 5,000,000 in 1,840 records.
- All 50,000 net-disbursement values match 80% of loan amount within 0.01.
- No date or snapshot column was found in the bureau schema.
- All installment start dates occur after their recorded disbursal dates.
- Raw CSVs remain unchanged, and no model has been trained.

## 5. Hypotheses and unknowns

The following are hypotheses, not verified facts:

- The intended prediction point is before loan approval or disbursement.
- `principal_outstanding` may represent a later account state.
- Charges and net disbursement may be determined during or after the lending decision.
- Repeated maximum outstanding balances may indicate capping or clipping.
- `principal_outstanding = -1` may be a sentinel.
- The observed 80% relationship may reflect a data-generation rule.

Unresolved target questions:

1. What business event does `default = True` represent?
2. Does it describe an existing status or a future event?
3. What threshold or event creates a positive label?
4. What is the target observation window and prediction horizon?
5. When was the label assigned?
6. Have negative labels had sufficient follow-up time?
7. How are active, immature, or censored loans handled?
8. Was the label generated using any supplied feature or later account state?

## 6. Proposed prediction point

**Working assumption only:** estimate risk before loan approval or disbursement.

This is an audit assumption, not a verified source-data fact. Disbursal and installment dates do not establish when other fields were collected or when the target was assigned.

No feature is certified as point-in-time safe by this review.

## 7. Feature-timing and leakage matrix

Classification:
- **Candidate, unverified:** potentially available at the assumed prediction point, but evidence is missing.
- **Unresolved:** meaning or timing requires further evidence.
- **Exclude initially:** conservative exclusion because of leakage risk.
- **Never predictor:** identifier or target excluded from ordinary model inputs.

### A. Customer attributes

| Field | Initial decision | Evidence needed |
|---|---|---|
| `age` | Candidate, unverified | Application snapshot and age reference date |
| `gender` | Candidate, unverified | Source definition, timing, and appropriate-use review |
| `marital_status` | Candidate, unverified | Application snapshot |
| `employment_status` | Candidate, unverified | Application snapshot and category definition |
| `income` | Candidate, unverified | Units, income period, and reference date |
| `number_of_dependants` | Candidate, unverified | Definition and reference date |
| `residence_type` | Candidate, unverified | Definition, timestamp, and missingness policy |
| `years_at_current_address` | Candidate, unverified | Calculation method and reference date |
| `city`, `state`, `zipcode` | Unresolved | Timing, usefulness, privacy, and generalization review |

### B. Loan application and terms

| Field | Initial decision | Evidence needed |
|---|---|---|
| `loan_purpose` | Candidate, unverified | Application schema or source documentation |
| `loan_type` | Candidate, unverified | Definition and decision workflow |
| `bank_balance_at_application` | Candidate, unverified | Measurement method and timestamp |
| `sanction_amount` | Unresolved | Requested versus approved meaning and timestamp |
| `loan_amount` | Unresolved | Requested versus approved meaning and timestamp |
| `loan_tenure_months` | Unresolved | Requested versus approved meaning and timestamp |

### C. Bureau attributes

| Field | Initial decision | Evidence needed |
|---|---|---|
| `number_of_open_accounts` | Unresolved, high scrutiny | Snapshot date and definition |
| `number_of_closed_accounts` | Unresolved, high scrutiny | Snapshot date and definition |
| `total_loan_months` | Unresolved, high scrutiny | Definition and measurement window |
| `delinquent_months` | Unresolved, high scrutiny | Definition, reference period, and snapshot date |
| `total_dpd` | Unresolved, high scrutiny | DPD definition, aggregation window, and snapshot date |
| `enquiry_count` | Unresolved, high scrutiny | Snapshot date and counting window |
| `credit_utilization_ratio` | Unresolved, high scrutiny | Calculation definition and reference date |

Bureau features require snapshot dates and measurement windows. Their presence in a joined table does not prove that they were available before the lending decision. Delinquency measures require particular scrutiny for overlap with the target period.

### D. Process and outcome fields

| Field | Initial decision | Reason |
|---|---|---|
| `principal_outstanding` | Exclude initially | Potential later account-state leakage |
| `processing_fee` | Exclude initially | May be set during or after approval |
| `gst` | Exclude initially | May be determined during loan processing |
| `net_disbursement` | Exclude initially | May be calculated during or after disbursement |
| `disbursal_date` | Do not use as an initial predictor | Event timing and intended validation design need review |
| `installment_start_dt` | Do not use as an initial predictor | Recorded event date follows disbursal in all audited rows |

### E. Identifiers and target

| Field | Decision | Reason |
|---|---|---|
| `cust_id` | Never an ordinary predictor | Join and audit identifier |
| `loan_id` | Never an ordinary predictor | Record identifier |
| `default` | Label only | Must never predict itself |

No field is permanently declared invalid. Reconsideration requires evidence of its definition and availability at the chosen prediction timestamp.

## 8. Data-quality findings and current handling

| Finding | Evidence | Current handling |
|---|---|---|
| Missing residence type | 62 values | Preserve; choose a justified preprocessing policy later |
| Zero-loan records | 8 with `principal_outstanding = -1` | Flag; do not silently delete or recode |
| Zero-loan label association | All 8 labels are `False` | Record association only; do not infer target logic |
| Processing-fee anomalies | 7 fees exceed loan amounts | Investigate definition and units; preserve raw values |
| Repeated outstanding maximum | 1,840 values equal 5,000,000 | Capping is only a hypothesis; preserve values |
| Net-disbursement relationship | 50,000 of 50,000 match 80% within 0.01 | Observed relationship, not a verified banking rule |
| Bureau timing | No snapshot/date column | Timing unresolved |
| Date ordering | Installment starts after disbursal in all audited rows | Structural observation only |
| Key relationships | All IDs match and joins preserve row counts | Basic integrity passes, not temporal validity |

No automatic deletion, capping, imputation, or rewriting of raw records is authorized by these observations.

## 9. Leakage-prevention policy

1. Treat `default` as an undocumented candidate label, not a verified future outcome.
2. Do not certify feature safety based solely on column names.
3. Exclude identifiers from ordinary model inputs.
4. Never use `default` as a predictor.
5. Keep high-risk process and account-state fields out of the initial feature set.
6. Require evidence of bureau snapshot timing before considering bureau features.
7. Split data before fitting learned preprocessing.
8. Fit imputers, encoders, scalers, and feature selection on training data only.
9. Choose validation design only after clarifying the intended prediction setting and record timing.
10. Preserve raw files and document justified transformations and exclusions.
11. Disclose target and feature-lineage limitations in any future experiment.
12. Do not present educational classification results as validated lending-risk performance.

## 10. Modelling-readiness decision

**Outcome B: Limited educational classification may be considered later under explicit assumptions.**

The evidence establishes a structurally valid binary column and basic key integrity. It does not establish target semantics, label maturity, or point-in-time feature validity.

Any later experiment must be framed as learning from an undocumented supplied label. It cannot substantiate a claim that future-default prediction has been validated for a real lending workflow.

Before training:
1. Seek authoritative target definition and generation logic.
2. Seek the observation window and label-assignment date.
3. Establish the intended prediction point.
4. Obtain feature definitions and timestamps, especially for bureau fields.
5. Document treatment of suspicious records without silently modifying raw data.
6. Design validation consistent with what the dataset can establish.
7. Record remaining assumptions in the README and experiment report.

If a defensible real-world future-default claim is required, use Outcome C until critical provenance gaps are resolved.

## 11. Interview learning notes

**Why is a valid binary target not necessarily a valid prediction target?**
A column can be complete and correctly typed while its business definition, event timing, and observation window remain unknown.

**Why can a bureau join still leak information?**
Key integrity does not prove that the bureau snapshot predates the prediction timestamp.

**Why not automatically delete the zero-loan records?**
Their operational meaning is unknown. Deletion without evidence could introduce undocumented selection bias.

**Why is the 80% relationship not automatically a business rule?**
It is an observed pattern in this dataset; the generation process and business rationale are undocumented.

**Why exclude principal outstanding initially?**
It may represent account information observed after the prediction point.

**Why is label maturity important?**
A negative label may be premature if insufficient time has elapsed to observe the outcome.

**What does Outcome B permit?**
A clearly labelled educational experiment, not a validated future-default prediction claim.

**What is the next technical priority?**
Resolve target provenance and feature timing before selecting a definitive feature set or reporting model performance.

## 12. Day 6 completion checklist

- [x] Review README and Day 3 to Day 5 documentation.
- [x] Inspect target and feature-timing scripts.
- [x] Inspect relevant Day 3 notebook cells.
- [x] Confirm CSV schemas.
- [x] Re-run read-only quality checks.
- [x] Separate facts, hypotheses, and unknowns.
- [x] Build feature-timing and leakage matrix.
- [x] Select provisional modelling-readiness outcome.
- [ ] Review document diff.
- [ ] Re-run tests and validation.
- [ ] Review Git status and preserve unrelated changes.
- [ ] Commit only the reviewed Day 6 document.

No model has been trained. No raw data has been changed.
