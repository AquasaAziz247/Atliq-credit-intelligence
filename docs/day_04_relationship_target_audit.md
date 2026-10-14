# AtliQ Credit Intelligence

## Day 4: Relationship, Target, and Feature-Timing Audit

### 1. Scope

This audit investigates dataset relationships, candidate target semantics, feature timing, and risks that must be resolved before modelling.

The project is an educational portfolio prototype. The source data does not include a verified data dictionary or documented target-generation process.

### 2. Dataset relationships

Three source files were inspected:

| Dataset         |   Rows | Key     | Key findings                              |
| --------------- | -----: | ------- | ----------------------------------------- |
| customers.csv   | 50,000 | cust_id | 50,000 distinct, non-missing customer IDs |
| loans.csv       | 50,000 | loan_id | 50,000 distinct, non-missing loan IDs     |
| bureau_data.csv | 50,000 | cust_id | 50,000 distinct, non-missing customer IDs |

All 50,000 customer IDs in the loans dataset match customer records. All 50,000 customer IDs in the bureau dataset also match customer records. No unmatched customer IDs were observed in either direction.

Each customer has exactly one loan record in this dataset.

Temporary left joins from loans to customers and from loans to bureau data passed pandas `many_to_one` validation. Both joins preserved 50,000 rows and matched all 50,000 records.

These findings establish basic identifier and join integrity. They do not establish point-in-time feature validity or prove that the supplied data represents a realistic lending population.

### 3. Candidate target investigation

The candidate target is `loans.default`.

| Measure                   | Observed result |
| ------------------------- | --------------: |
| Total records             |          50,000 |
| False labels              |          45,703 |
| True labels               |           4,297 |
| Missing labels            |               0 |
| Positive-label proportion |          8.594% |

The column has Boolean values. Disbursal dates range from 2019-07-24 to 2024-07-22. Installment start dates range from 2019-07-25 to 2024-08-20.

The observed positive-label proportion by disbursal year ranges from approximately 8.39% to 8.76%.

The target-generation logic, business definition, observation window, and prediction horizon remain undocumented. The presence of bureau fields such as `delinquent_months` and `total_dpd` does not establish that either field defines `default`.

**Decision:** Treat `default` as a provisional candidate target. Do not claim validated future-default prediction.

### 4. Feature timing and leakage policy

The intended prediction point is provisionally before loan approval or disbursement. This is an audit assumption, not a verified source-data fact.

#### Potential application-time candidates

- Customer attributes: `age`, `gender`, `marital_status`, `employment_status`, `income`, `number_of_dependants`, `residence_type`, `years_at_current_address`.
- Loan attributes: `loan_purpose`, `loan_type`, `bank_balance_at_application`.

Their collection timing and definitions still require verification.

#### Timing or definition uncertain

- `sanction_amount`, `loan_amount`, `loan_tenure_months`
- `city`, `state`, `zipcode`
- `number_of_open_accounts`, `number_of_closed_accounts`, `total_loan_months`
- `delinquent_months`, `total_dpd`, `enquiry_count`, `credit_utilization_ratio`
- `disbursal_date`, `installment_start_dt`

Bureau features require snapshot dates and measurement windows. Geographic features require a separate usefulness, privacy, and generalization review.

#### Exclude from the initial feature set

- `principal_outstanding`
- `processing_fee`, `gst`, `net_disbursement`

These fields have potential timing or business-process leakage risks. Reconsideration requires evidence that they were available at the intended prediction point.

#### Identifiers and target

- Exclude `loan_id` and `cust_id` from ordinary model inputs.
- Never include `default` as a predictor of itself.

### 5. Additional structural findings

All 50,000 installment start dates occur after their recorded disbursal dates. The observed delay ranges from 1 to 30 days, with a mean of approximately 15.54 days.

`residence_type` has 62 missing values. Preserve these missing values until a justified preprocessing policy is selected.

An earlier audit found that `net_disbursement` matches approximately 80% of `loan_amount` within 0.01 for all 50,000 records. This is an observed relationship, not a verified business rule.

The earlier audit also identified zero-loan anomalies, negative principal values, unusually large outstanding balances, and seven processing fees exceeding loan amounts. Raw values remain unchanged.

### 6. Modelling readiness decision

**Decision: Not ready for a defensible future-default model.**

The datasets have promising basic key integrity and complete candidate target labels, but the target definition, observation horizon, and feature collection timestamps remain unresolved.

The project may proceed with further data validation and leakage-safe pipeline development. Any future modelling experiment must clearly disclose these limitations and must not be presented as a validated lending-risk system.

### 7. Next actions

1. Add automated tests for identifier uniqueness, referential integrity, join cardinality, and target validation.
2. Re-run the audits and tests.
3. Review the complete diff and preserve unrelated Day 2 notebook changes and the backup audit script.
4. Commit only reviewed, intended Day 4 files.
5. Do not push or claim a validated model without further evidence.
