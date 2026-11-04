
import streamlit as st
import pandas as pd
from sqlalchemy import text

from db_connection import get_connection
from styles import apply_custom_styles
from issue_prioritization import (
    get_issue_severity,
    get_all_issue_details
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Data Quality Issues",
    page_icon="⚠️",
    layout="wide"
)

apply_custom_styles()


# ==========================================
# PAGE HEADER
# ==========================================

st.title("Data Quality Issues")
st.caption(
    "Review and prioritize marketing records that require attention."
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_issues():
    query = text("SELECT * FROM DataQualityIssues")
    return pd.read_sql(query, get_connection())


try:

    df = load_issues()

    df["severity"] = df.apply(get_issue_severity, axis=1)
    df["issue_details"] = df.apply(get_all_issue_details, axis=1)
    df["issue_count"] = df["issue_details"].apply(len)

    df["issue_type"] = df["issue_details"].apply(
        lambda issues: ", ".join(issue[0] for issue in issues)
    )

    df = df.sort_values(
        by=["issue_count", "severity"],
        ascending=[False, True]
    )


    # ==========================================
    # REVIEW SUMMARY
    # ==========================================

    high_count = (df["severity"] == "High").sum()
    medium_count = (df["severity"] == "Medium").sum()
    low_count = (df["severity"] == "Low").sum()

    st.subheader("Review Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Records Requiring Review", f"{len(df):,}")
    col2.metric("High Priority", f"{high_count:,}")
    col3.metric("Medium Priority", f"{medium_count:,}")
    col4.metric("Low Priority", f"{low_count:,}")


    st.divider()


    # ==========================================
    # FILTERS
    # ==========================================

    st.subheader("Find Records")

    issue_columns = {
        "Missing Company": "missing_company_name",
        "Missing Email": "missing_email",
        "Missing Job Title": "missing_job_title",
        "Missing Campaign": "missing_campaign_name",
        "Invalid Email": "invalid_email",
        "Duplicate Email": "duplicate_email",
        "Company Name Inconsistency": "company_inconsistent"
    }

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        selected_issue = st.selectbox(
            "Issue Type",
            ["All Issues"] + list(issue_columns.keys())
        )

    with filter_col2:
        selected_severity = st.multiselect(
            "Priority",
            ["High", "Medium", "Low"],
            placeholder="All priority levels"
        )

    filtered_df = df.copy()

    if selected_severity:
        filtered_df = filtered_df[
            filtered_df["severity"].isin(selected_severity)
        ]

    if selected_issue != "All Issues":
        column = issue_columns[selected_issue]

        filtered_df = filtered_df[
            filtered_df[column].astype(int) == 1
        ]


    st.caption(
        f"Showing {len(filtered_df):,} of {len(df):,} records"
    )


    # ==========================================
    # RECORD TABLE
    # ==========================================

    st.subheader("Flagged Records")

    display_columns = [
        "record_id",
        "company_name",
        "email",
        "issue_count",
        "issue_type",
        "severity"
    ]

    if not filtered_df.empty:

        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            hide_index=True,
            height=420,
            column_config={
                "record_id": st.column_config.TextColumn(
                    "Record ID",
                    width="medium"
                ),
                "company_name": st.column_config.TextColumn(
                    "Company",
                    width="medium"
                ),
                "email": st.column_config.TextColumn(
                    "Email",
                    width="large"
                ),
                "issue_count": st.column_config.NumberColumn(
                    "Issues",
                    width="small"
                ),
                "issue_type": st.column_config.TextColumn(
                    "Detected Issues",
                    width="large"
                ),
                "severity": st.column_config.TextColumn(
                    "Priority",
                    width="small"
                )
            }
        )


        # ==========================================
        # INVESTIGATE A RECORD
        # ==========================================

        st.divider()

        st.subheader("Investigate a Record")

        record_options = filtered_df["record_id"].tolist()

        def get_record_label(record_id):

            record = filtered_df[
                filtered_df["record_id"] == record_id
            ].iloc[0]

            company = record["company_name"]

            if pd.isna(company):
                company = "Company not provided"

            return f"{record_id} — {company}"

        selected_record_id = st.selectbox(
            "Select a record",
            options=record_options,
            format_func=get_record_label
        )

        if st.button(
            "Investigate Record",
            type="primary"
        ):
            st.session_state["selected_record_id"] = selected_record_id
            st.switch_page("pages/3_Record_Investigation.py")


    else:

        st.info(
            "No records match your selected filters. "
            "Try adjusting your filters."
        )


except Exception as e:

    st.error(f"Unable to load data quality issues: {e}")
    st.exception(e)
