
import pandas as pd
import numpy as np
import random
from pathlib import Path

# Make the dataset reproducible
random.seed(42)
np.random.seed(42)

# Number of marketing records
NUM_RECORDS = 2000

# Sample business data
companies = [
    "Acme Technologies", "Global Solutions", "BluePeak Systems",
    "Vertex Consulting", "NexaSoft", "BrightPath Inc.",
    "Summit Enterprises", "CloudBridge", "Apex Digital",
    "Northstar Technologies", "Innovate Solutions",
    "Pioneer Systems", "Crestview Group", "Evergreen Software",
    "Orion Technologies"
]

first_names = [
    "John", "Sarah", "Michael", "Emily", "David",
    "Jessica", "Robert", "Amanda", "Daniel", "Sophia",
    "James", "Olivia", "William", "Emma", "Alexander"
]

last_names = [
    "Smith", "Johnson", "Brown", "Davis", "Wilson",
    "Taylor", "Anderson", "Thomas", "Moore", "Martin"
]

job_titles = [
    "Marketing Manager", "Finance Director",
    "IT Manager", "Operations Manager",
    "Chief Financial Officer", "Business Analyst",
    "Procurement Manager", "HR Director",
    "Sales Manager", "Accountant"
]

lead_sources = [
    "Website", "Webinar", "Email Campaign",
    "LinkedIn", "Referral", "Paid Search"
]

campaigns = [
    "Expense Automation Campaign",
    "Travel Management Webinar",
    "Finance Transformation",
    "Cloud Solutions Campaign",
    "Customer Success Campaign",
    "Digital Transformation"
]

regions = ["North America", "Europe", "Asia Pacific", "Latin America"]

lifecycle_stages = ["Lead", "MQL", "SQL", "Customer"]

products = [
    "Expense Management", "Travel Management",
    "Invoice Management", "Multiple Products"
]

consent_statuses = ["Opted In", "Opted Out", "Pending"]

# Generate clean baseline records
records = []

for i in range(NUM_RECORDS):

    company = random.choice(companies)
    first = random.choice(first_names)
    last = random.choice(last_names)

    email = (
        f"{first.lower()}.{last.lower()}"
        f"{i}@{company.lower().replace(' ', '').replace('.', '')}.com"
    )

    created_date = (
        pd.Timestamp("2025-01-01")
        + pd.Timedelta(days=random.randint(0, 300))
    )

    last_engagement = created_date + pd.Timedelta(
        days=random.randint(0, 60)
    )

    records.append({
        "record_id": f"LEAD{i + 1:05d}",
        "company_name": company,
        "first_name": first,
        "last_name": last,
        "email": email,
        "job_title": random.choice(job_titles),
        "lead_source": random.choice(lead_sources),
        "campaign_name": random.choice(campaigns),
        "region": random.choice(regions),
        "created_date": created_date,
        "last_engagement_date": last_engagement,
        "lifecycle_stage": random.choice(lifecycle_stages),
        "product_interest": random.choice(products),
        "consent_status": random.choice(consent_statuses)
    })

df = pd.DataFrame(records)

# Introduce intentional data-quality issues

# 1. Missing values
for column, count in {
    "company_name": 45,
    "email": 60,
    "job_title": 90,
    "campaign_name": 75
}.items():
    indices = random.sample(list(df.index), count)
    df.loc[indices, column] = np.nan

# 2. Invalid email addresses
invalid_email_indices = random.sample(list(df.index), 40)

for idx in invalid_email_indices:
    df.loc[idx, "email"] = random.choice([
        "invalid-email",
        "missingdomain@",
        "user.example.com",
        "@example.com"
    ])

# 3. Inconsistent company naming
company_variations = {
    "Acme Technologies": "ACME TECHNOLOGIES",
    "Global Solutions": "global solutions",
    "NexaSoft": "Nexa Soft",
    "BrightPath Inc.": "BrightPath INC",
    "Apex Digital": "APEX DIGITAL"
}

for original, variation in company_variations.items():
    indices = df.index[
        df["company_name"] == original
    ].tolist()

    selected = random.sample(
        indices,
        min(15, len(indices))
    )

    df.loc[selected, "company_name"] = variation

# 4. Duplicate records
duplicate_rows = df.sample(n=50, random_state=42).copy()
duplicate_rows["record_id"] = [
    f"DUP{i + 1:05d}" for i in range(len(duplicate_rows))
]

df = pd.concat(
    [df, duplicate_rows],
    ignore_index=True
)

# Shuffle records
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the raw dataset
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "raw_marketing_leads.csv"

df.to_csv(output_file, index=False)

# Display dataset information
print("\nMARKETING DATASET GENERATED SUCCESSFULLY")
print("-----------------------------------------")
print(f"Total records: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Output file: {output_file}")

print("\nMissing values by column:")
print(df.isnull().sum())

print("\nSample records:")
print(df.head())

print("\nDataset generation completed!")
