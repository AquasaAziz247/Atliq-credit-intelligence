
"""Structural data contracts for the AtliQ Credit Intelligence CSVs.

These contracts validate observed schema and integrity requirements.
They do not define the business meaning of the default target.
"""

CUSTOMER_COLUMNS = {
    "cust_id",
    "age",
    "gender",
    "marital_status",
    "employment_status",
    "income",
    "number_of_dependants",
    "residence_type",
    "years_at_current_address",
    "city",
    "state",
    "zipcode",
}

LOAN_COLUMNS = {
    "loan_id",
    "cust_id",
    "loan_purpose",
    "loan_type",
    "sanction_amount",
    "loan_amount",
    "processing_fee",
    "gst",
    "net_disbursement",
    "loan_tenure_months",
    "principal_outstanding",
    "bank_balance_at_application",
    "disbursal_date",
    "installment_start_dt",
    "default",
}

BUREAU_COLUMNS = {
    "cust_id",
    "number_of_open_accounts",
    "number_of_closed_accounts",
    "total_loan_months",
    "delinquent_months",
    "total_dpd",
    "enquiry_count",
    "credit_utilization_ratio",
}

# Only residence_type is known to have missing values in the current audit.
# This is a documented observation, not a claim that missingness is always valid.
ALLOWED_MISSINGNESS = {
    "customers": {"residence_type"},
    "loans": set(),
    "bureau": set(),
}

# Identifiers expected to be unique within their respective source tables.
PRIMARY_KEYS = {
    "customers": "cust_id",
    "loans": "loan_id",
    "bureau": "cust_id",
}
