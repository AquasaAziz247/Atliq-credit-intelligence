# AtliQ Credit Intelligence

## Day 3: Data Decisions and Feature Policy

### 1. Project objective

The proposed objective is to investigate whether the supplied data can support a credit-risk prediction model using information available before a lending decision.

This is an educational portfolio prototype. The dataset's target-generation logic, observation horizon, and feature collection timestamps are undocumented.

### 2. Target definition

- Candidate target: `default` in `loans.csv`.
- Observed records: 50,000.
- `default = False`: 45,703.
- `default = True`: 4,297.
- Observed positive-label proportion: 8.594%.
- Confirmed business definition: unavailable.
- Confirmed prediction horizon: unavailable.

**Decision:** Treat `default` as a candidate target only. Do not claim the dataset establishes future-default prediction until its semantics and observation window are verified.

### 3. Data quality decisions

| Finding                       | Evidence                                                                         | Current decision                                                                  |
| ----------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Missing residence type        | 62 missing values in `customers.csv`                                             | Preserve missingness; investigate before choosing an imputation strategy.         |
| Zero-loan records             | 8 records have zero loan-related amounts and `principal_outstanding = -1`        | Flag for investigation; do not silently delete or recode.                         |
| Net disbursement relationship | All 50,000 records match `0.80 * loan_amount` within 0.01                        | Document as an observed relationship, not a verified business rule.               |
| Outstanding-balance maximum   | 1,840 records equal 5,000,000                                                    | Investigate possible capping; preserve raw values.                                |
| Processing fee anomalies      | 7 records have `processing_fee > loan_amount`                                    | Flag for investigation; do not assume values are erroneous.                       |
| Date validation               | No unparseable or missing dates, and no installment start dates before disbursal | Structural checks passed; event timing relative to prediction remains unresolved. |
| Record integrity              | No exact duplicate rows or unmatched customer IDs reported in the audit          | Basic integrity checks passed; point-in-time validity is not established.         |

### 4. Preliminary feature policy

The intended prediction point is provisionally defined as before loan approval or disbursement.

#### Identifiers

Exclude `loan_id` and `cust_id` from model inputs. Retain them where needed for joins, audit trails, and record-level validation.

#### Potential application-time candidates

`age`, `gender`, `marital_status`, `employment_status`, `income`, `number_of_dependants`, `residence_type`, `years_at_current_address`, `loan_purpose`, `loan_type`, and `bank_balance_at_application`.

These are candidates only. Their actual availability and definitions must be verified.

#### Features requiring additional timing or definition checks

- `sanction_amount`
- `loan_amount`
- `loan_tenure_months`
- `city`, `state`, `zipcode`
- `number_of_open_accounts`
- `number_of_closed_accounts`
- `total_loan_months`
- `delinquent_months`
- `total_dpd`
- `enquiry_count`
- `credit_utilization_ratio`
- `disbursal_date`
- `installment_start_dt`

Bureau attributes require a documented snapshot date and measurement window. Geographic fields require a separate usefulness, privacy, and generalization review.

#### High-risk or excluded from the initial feature set

- `default`: candidate target, never an input when predicting default.
- `principal_outstanding`: possible later account-state information.
- `processing_fee`, `gst`, `net_disbursement`: may be determined during or after approval or disbursement.

These fields are not declared permanently invalid. Reconsideration requires evidence that their values were available at the intended prediction point.

### 5. Leakage prevention rules

1. Define the prediction point and target observation window before training.
2. Verify feature timestamps and business meanings where possible.
3. Do not use the target as an input feature.
4. Do not assume customer-level joins guarantee point-in-time validity.
5. Split data before fitting imputers, encoders, scalers, or other learned transformations.
6. Fit learned preprocessing on training data only.
7. Keep raw CSV files unchanged.
8. Document all exclusions, imputations, transformations, and assumptions.
9. If target semantics or critical feature timing cannot be established, disclose the limitation rather than presenting the model as validated.

### 6. Current project status

- Raw data audit completed.
- Initial EDA completed.
- Feature availability and leakage risks inventoried provisionally.
- Suspicious records investigated without modifying raw CSVs.
- Target semantics and feature timestamps remain unresolved.
- No model training has been performed.

### 7. Next actions

1. Investigate available evidence about target and feature timing.
2. Design reproducible cleaning functions only for justified decisions.
3. Add tests for transformations and data-integrity assumptions.
4. Update the README with project scope, limitations, and reproducible instructions.
