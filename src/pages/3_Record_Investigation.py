
import streamlit as st
import pandas as pd
from sqlalchemy import text

from db_connection import get_connection
from styles import apply_custom_styles


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Record Investigation",
    page_icon="🔍",
    layout="wide"
)

apply_custom_styles()


# ==========================================
# PAGE HEADER
# ==========================================

st.title("Record Investigation")
st.caption(
    "Review individual marketing records, understand detected "
    "data-quality issues, and identify corrective actions."
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_issues():

    query = text("""
        SELECT *
        FROM DataQualityIssues
        ORDER BY record_id
    """)

    return pd.read_sql(query, get_connection())


try:

    df = load_issues()

    if df.empty:
        st.info("No records are currently available for investigation.")
        st.stop()

    # ==========================================
    # RECORD SELECTION
    # ==========================================

    st.subheader("Select a Record")

    record_ids = sorted(
        df["record_id"].dropna().unique().tolist()
    )

    # Use the record selected on the Data Quality Issues page
    previous_selection = st.session_state.get(
        "selected_record_id"
    )

    if previous_selection in record_ids:
        default_index = record_ids.index(previous_selection)
    else:
        default_index = 0

    selected_id = st.selectbox(
        "Choose a record ID",
        options=record_ids,
        index=default_index,
        key="investigation_record_selector"
    )

    # Clear the transferred selection after the widget is initialized
    if "selected_record_id" in st.session_state:
        st.session_state.pop("selected_record_id")

    record = df[
        df["record_id"] == selected_id
    ].iloc[0]


    # ==========================================
    # DETECTED ISSUES
    # ==========================================

    issue_definitions = {
        "missing_company_name": (
            "Missing Company Name",
            "Company information is missing.",
            "Provide or verify the company name."
        ),
        "missing_email": (
            "Missing Email",
            "Contact cannot be reached through email.",
            "Verify the contact's email address."
        ),
        "missing_job_title": (
            "Missing Job Title",
            "Contact role information is missing.",
            "Enrich the record with the contact's job title."
        ),
        "missing_campaign_name": (
            "Missing Campaign",
            "Campaign attribution may be incomplete.",
            "Identify and associate the originating campaign."
        ),
        "invalid_email": (
            "Invalid Email",
            "Email format is invalid and may prevent delivery.",
            "Verify the email address and correct its format."
        ),
        "duplicate_email": (
            "Duplicate Email",
            "The email appears in multiple records.",
            "Review the associated records before deciding whether to merge them."
        ),
        "company_inconsistent": (
            "Company Name Inconsistency",
            "Company naming variations may fragment reporting.",
            "Compare the company name against the approved naming convention."
        )
    }

    detected_issues = []

    for column, details in issue_definitions.items():

        if column in df.columns and pd.notna(record[column]):

            if int(record[column]) == 1:
                detected_issues.append(details)


    # ==========================================
    # RECORD OVERVIEW
    # ==========================================

    st.divider()
    st.subheader("Record Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Record ID",
        selected_id
    )

    quality_score = record["quality_score"]

    col2.metric(
        "Quality Score",
        f"{quality_score:.0f}/100"
        if pd.notna(quality_score)
        else "Not available"
    )

    col3.metric(
        "Issues Detected",
        len(detected_issues)
    )


    # ==========================================
    # CONTACT INFORMATION
    # ==========================================

    st.divider()
    st.subheader("Contact Information")

    detail_columns = [
        "company_name",
        "first_name",
        "last_name",
        "email",
        "job_title",
        "lead_source",
        "campaign_name",
        "region",
        "lifecycle_stage",
        "product_interest",
        "consent_status"
    ]

    available_columns = [
        column for column in detail_columns
        if column in df.columns
    ]

    left, right = st.columns(2)

    for index, column in enumerate(available_columns):

        value = record[column]

        if pd.isna(value):
            value = "Not provided"

        with (left if index % 2 == 0 else right):

            st.markdown(
                f"**{column.replace('_', ' ').title()}**"
            )

            st.write(str(value))


    # ==========================================
    # ISSUE DETAILS AND RECOMMENDATIONS
    # ==========================================

    st.divider()
    st.subheader("Detected Issues & Recommended Actions")

    if detected_issues:

        for issue, description, recommendation in detected_issues:

            with st.expander(issue, expanded=True):

                st.markdown("**What was detected**")
                st.write(description)

                st.markdown("**Recommended action**")
                st.info(recommendation)

    else:

        st.success(
            "No quality issues detected for this record."
        )


except Exception as e:

    st.error(f"Unable to investigate record: {e}")
    st.exception(e)
