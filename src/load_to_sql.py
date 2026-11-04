import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pathlib import Path

# SQL Server connection details
server = r"localhost\SQLEXPRESS"
database = "MarketingDataHealth"
driver = "ODBC Driver 18 for SQL Server"

# Windows Authentication
connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

# Encode the connection string for SQLAlchemy
connection_url = (
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(connection_string)
)

# Create database connection
engine = create_engine(connection_url)

# Test the connection
with engine.connect() as connection:
    print("Successfully connected to SQL Server!")




# Locate the project data folder
project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"

# Define datasets and their SQL table names
datasets = {
    "MarketingLeads": "raw_marketing_leads.csv",
    "DataQualityIssues": "quality_issues.csv",
    "DataQualitySummary": "quality_summary.csv"
}

# Load each CSV into SQL Server
for table_name, file_name in datasets.items():

    file_path = data_folder / file_name

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(df)} records into {table_name}")