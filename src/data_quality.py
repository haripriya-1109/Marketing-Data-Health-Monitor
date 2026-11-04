
import pandas as pd
import re
from pathlib import Path

# --------------------------------------------------
# 1. LOAD THE DATASET
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "data" / "raw_marketing_leads.csv"
OUTPUT_FILE = PROJECT_DIR / "data" / "quality_issues.csv"
SUMMARY_FILE = PROJECT_DIR / "data" / "quality_summary.csv"

df = pd.read_csv(INPUT_FILE)

print("DATA QUALITY ANALYSIS STARTED")
print("--------------------------------")
print(f"Records loaded: {len(df)}")


# --------------------------------------------------
# 2. CHECK DATA COMPLETENESS
# --------------------------------------------------

required_columns = [
    "company_name",
    "email",
    "job_title",
    "campaign_name"
]

missing_counts = df[required_columns].isnull().sum()

completeness = (
    (len(df) - missing_counts) / len(df) * 100
).round(2)

print("\nDATA COMPLETENESS")
print("-----------------")

for column in required_columns:
    print(
        f"{column}: {missing_counts[column]} missing "
        f"({100 - completeness[column]:.2f}%)"
    )


# --------------------------------------------------
# 3. VALIDATE EMAIL ADDRESSES
# --------------------------------------------------

email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

df["email_normalized"] = (
    df["email"]
    .astype("string")
    .str.strip()
    .str.lower()
)

df["invalid_email"] = (
    df["email_normalized"].notna()
    & ~df["email_normalized"].str.match(
        email_pattern, na=False
    )
)

invalid_email_count = int(df["invalid_email"].sum())

print("\nEMAIL VALIDATION")
print("----------------")
print(f"Invalid emails: {invalid_email_count}")


# --------------------------------------------------
# 4. DETECT DUPLICATE CONTACT RECORDS
# --------------------------------------------------

df["duplicate_email"] = (
    df["email_normalized"].notna()
    & df["email_normalized"].str.match(
        email_pattern, na=False
    )
    & df["email_normalized"].duplicated(keep="first")
)

duplicate_count = int(df["duplicate_email"].sum())

print("\nDUPLICATE DETECTION")
print("-------------------")
print(f"Additional records with duplicate emails: {duplicate_count}")


# --------------------------------------------------
# 5. IDENTIFY COMPANY NAME INCONSISTENCIES
# --------------------------------------------------

def normalize_company(company):
    """
    Standardize company names for comparison.
    Removes spaces, punctuation and case differences.
    """

    if pd.isna(company):
        return None

    return re.sub(
        r"[^a-zA-Z0-9]",
        "",
        str(company).lower()
    )


df["company_normalized"] = df["company_name"].apply(
    normalize_company
)

company_variation_counts = (
    df.groupby("company_normalized")["company_name"]
    .nunique()
)

inconsistent_companies = company_variation_counts[
    company_variation_counts > 1
].index

df["company_inconsistent"] = (
    df["company_name"].notna()
    & df["company_normalized"].isin(inconsistent_companies)
    & df["company_name"].str.strip().ne(
        df["company_normalized"].map(
            df.groupby("company_normalized")["company_name"]
            .agg(lambda x: x.value_counts().index[0])
        )
    )
)

inconsistent_count = int(df["company_inconsistent"].sum())

print("\nCOMPANY STANDARDIZATION")
print("-----------------------")
print(f"Records with company naming variations: {inconsistent_count}")


# --------------------------------------------------
# 6. GENERATE RECORD-LEVEL QUALITY FLAGS
# --------------------------------------------------

for column in required_columns:
    df[f"missing_{column}"] = df[column].isna()

issue_columns = [
    f"missing_{column}" for column in required_columns
] + [
    "invalid_email",
    "duplicate_email",
    "company_inconsistent"
]

df["total_issues"] = df[issue_columns].sum(axis=1)

df["requires_review"] = df["total_issues"] > 0


# --------------------------------------------------
# 7. CALCULATE RECORD-LEVEL QUALITY SCORES
# --------------------------------------------------

# Each record starts at 100.
# Deduct 20 points for each missing required field,
# invalid email, duplicate email or company variation.

df["quality_score"] = (
    100 - df["total_issues"] * 20
).clip(lower=0)

print("\nRECORD QUALITY")
print("--------------")
print(
    f"Average quality score: "
    f"{df['quality_score'].mean():.2f}/100"
)

print(
    f"Records requiring review: "
    f"{df['requires_review'].sum()}"
)


# --------------------------------------------------
# 8. CREATE OVERALL DATA QUALITY SUMMARY
# --------------------------------------------------

total_records = len(df)

summary = pd.DataFrame({
    "metric": [
        "Total Records",
        "Missing Company Names",
        "Missing Emails",
        "Missing Job Titles",
        "Missing Campaign Names",
        "Invalid Emails",
        "Duplicate Email Records",
        "Inconsistent Company Records",
        "Records Requiring Review",
        "Average Quality Score"
    ],

    "value": [
        total_records,
        int(missing_counts["company_name"]),
        int(missing_counts["email"]),
        int(missing_counts["job_title"]),
        int(missing_counts["campaign_name"]),
        invalid_email_count,
        duplicate_count,
        inconsistent_count,
        int(df["requires_review"].sum()),
        round(df["quality_score"].mean(), 2)
    ]
})


# --------------------------------------------------
# 9. EXPORT REPORTS
# --------------------------------------------------

# Export only records requiring attention.
issues_df = df[df["requires_review"]].copy()

issues_df.to_csv(OUTPUT_FILE, index=False)
summary.to_csv(SUMMARY_FILE, index=False)

print("\nREPORTS GENERATED")
print("-----------------")
print(f"Record-level report: {OUTPUT_FILE}")
print(f"Summary report: {SUMMARY_FILE}")

print("\nDATA QUALITY ANALYSIS COMPLETED!")
