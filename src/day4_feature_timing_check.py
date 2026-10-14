
"""Read-only checks for feature timing and leakage clues."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

customers = pd.read_csv(ROOT / "data" / "raw" / "customers.csv")
loans = pd.read_csv(ROOT / "data" / "raw" / "loans.csv")
bureau = pd.read_csv(ROOT / "data" / "raw" / "bureau_data.csv")

print("=== DATE ORDER CHECK ===")
disbursal = pd.to_datetime(loans["disbursal_date"], errors="coerce")
installment = pd.to_datetime(
    loans["installment_start_dt"], errors="coerce"
)

print(f"Installment before disbursal: {(installment < disbursal).sum()}")
print(f"Same-day installment start: {(installment == disbursal).sum()}")
print(f"Installment after disbursal: {(installment > disbursal).sum()}")
print(f"Days from disbursal to installment start:")
print((installment - disbursal).dt.days.describe().to_string())

print("\n=== CANDIDATE FEATURE MISSINGNESS ===")
for name, frame, columns in [
    ("customers", customers, [
        "age", "gender", "marital_status", "employment_status",
        "income", "number_of_dependants", "residence_type",
        "years_at_current_address", "city", "state", "zipcode",
    ]),
    ("loans", loans, [
        "loan_purpose", "loan_type", "sanction_amount", "loan_amount",
        "loan_tenure_months", "bank_balance_at_application",
        "processing_fee", "gst", "net_disbursement",
        "principal_outstanding",
    ]),
    ("bureau", bureau, [
        "number_of_open_accounts", "number_of_closed_accounts",
        "total_loan_months", "delinquent_months", "total_dpd",
        "enquiry_count", "credit_utilization_ratio",
    ]),
]:
    print(f"\n[{name}]")
    for column in columns:
        if column in frame.columns:
            print(
                f"{column}: missing={frame[column].isna().sum()}, "
                f"dtype={frame[column].dtype}, "
                f"unique={frame[column].nunique(dropna=True)}"
            )

print("\n=== BUREAU VALUE RANGES ===")
for column in [
    "number_of_open_accounts", "number_of_closed_accounts",
    "total_loan_months", "delinquent_months", "total_dpd",
    "enquiry_count", "credit_utilization_ratio",
]:
    if column in bureau.columns:
        print(f"\n{column}")
        print(bureau[column].describe().to_string())

print("\n=== LOAN AMOUNT RELATIONSHIPS ===")
for column in ["sanction_amount", "loan_amount", "processing_fee",
               "gst", "net_disbursement", "principal_outstanding"]:
    if column in loans.columns:
        print(f"\n{column}")
        print(loans[column].describe().to_string())

print("\n=== CHECK COMPLETE ===")
print("These are structural observations, not proof of feature availability.")
