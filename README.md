# Marketing Data Health Monitor

An interactive data quality monitoring dashboard built with Python, SQL Server, and Streamlit to identify, investigate, and prioritize issues in B2B marketing data.

## Project Overview

Marketing teams rely on accurate and consistent data to support campaign execution, audience segmentation, and customer engagement. Missing information, invalid email addresses, duplicate records, and inconsistent company names can affect data reliability.

This project demonstrates a data quality monitoring workflow using a synthetic marketing leads dataset. It identifies common data issues, assigns quality scores, prioritizes records for review, and provides an interactive dashboard for investigation.

## Project Presentation

- [View Case Study (PDF)](presentation/Marketing-Data-Health-Monitor%20PDF.pdf)
- [View PowerPoint](presentation/Marketing-Data-Health-Monitor%20PPT.pptx)

## Key Features

- **Data Overview:** Monitor total records, average quality score, and records requiring review.
- **Data Explorer:** Search and filter marketing records by company, email, region, lead source, and lifecycle stage.
- **Data Quality Monitoring:** Identify missing values, invalid email addresses, duplicate emails, and inconsistent company names.
- **Issue Prioritization:** Classify records by High, Medium, and Low severity.
- **Record Investigation:** Inspect individual records, understand detected issues, and view recommended corrective actions.
- **SQL Integration:** Store marketing records and quality findings in SQL Server and retrieve them for dashboard reporting.

## Technology Stack

- Python
- Pandas and NumPy
- Microsoft SQL Server Express
- SQLAlchemy and pyodbc
- Streamlit
- Plotly

## Dataset

The project uses a synthetic dataset of 2,050 marketing lead records across 14 fields.

The dataset intentionally includes data quality issues to simulate realistic marketing data challenges.

Issues evaluated include:
- Missing company names, email addresses, job titles, and campaign names
- Invalid email formats
- Duplicate email addresses
- Inconsistent company naming conventions

No real customer or company data is used.

## Key Findings

| Metric | Result |
|---|---:|
| Total records analyzed | 2,050 |
| Average data quality score | 95.72/100 |
| Records requiring review | 410 |
| Review rate | 20% |
| Invalid email records | 41 |
| Duplicate email records | 47 |
| Company-name inconsistencies | 77 |

### Issue Severity

- High: 150 records
- Medium: 181 records
- Low: 79 records

*Quality scores and severity classifications use illustrative, project-defined rules and are not official industry or company standards.*

## Project Structure

```text
Marketing-Data-Health-Monitor/
│
├── data/
│   ├── raw_marketing_leads.csv
│   ├── quality_issues.csv
│   └── quality_summary.csv
│
├── src/
│   ├── .streamlit/
│   │   └── config.toml
│   ├── pages/
│   │   ├── 1_Data_Explorer.py
│   │   ├── 2_Data_Quality_Issues.py
│   │   └── 3_Record_Investigation.py
│   ├── Home.py
│   ├── data_quality.py
│   ├── db_connection.py
│   ├── generate_data.py
│   ├── issue_prioritization.py
│   ├── load_to_sql.py
│   ├── navigation.py
│   ├── requirements.txt
│   └── styles.py
│
└── .gitignore
```

## Running the Application

### Prerequisites

- Python 3.13 or a compatible version
- Microsoft SQL Server Express
- SQL Server ODBC Driver 18
- A local SQL Server database named `MarketingDataHealth`

### Installation

1. Clone the repository:

```bash
git clone https://github.com/haripriya-1109/Marketing-Data-Health-Monitor.git
cd Marketing-Data-Health-Monitor
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r src/requirements.txt
```

4. Configure SQL Server Express and ensure the connection settings in `src/db_connection.py` match your local SQL Server instance. The project currently uses Windows Authentication.

5. Set up the `MarketingDataHealth` database and load the dataset and quality tables using the provided data-generation and SQL-loading scripts.

6. Launch the application from the project root:

```bash
streamlit run src/Home.py
```

Open `http://localhost:8501` in your browser.

## Future Enhancements

- Automated and scheduled data quality monitoring
- Configurable data quality thresholds and governance rules
- Enhanced duplicate detection and company-name standardization
- Data retention and consent management workflows
- Automated issue reporting and stakeholder notifications

## Project Purpose

This project explores how data quality monitoring, SQL-based validation, and interactive reporting can help marketing teams maintain reliable data and make better-informed operational decisions.
