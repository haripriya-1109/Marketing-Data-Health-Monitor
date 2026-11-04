
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text

from styles import apply_custom_styles
from db_connection import get_connection
from navigation import render_sidebar


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Marketing Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()


# ==========================================
# PAGE DEFINITIONS
# ==========================================

overview_page = st.Page(
    lambda: render_dashboard(),
    title="Overview",
    icon="🏠",
    default=True
)

data_explorer_page = st.Page(
    "pages/1_Data_Explorer.py",
    title="Data Explorer",
    icon="🔎"
)

data_quality_page = st.Page(
    "pages/2_Data_Quality_Issues.py",
    title="Data Quality",
    icon="⚠️"
)

record_investigation_page = st.Page(
    "pages/3_Record_Investigation.py",
    title="Record Investigation",
    icon="📋"
)

pages = [
    overview_page,
    data_explorer_page,
    data_quality_page,
    record_investigation_page
]


# ==========================================
# CUSTOM NAVIGATION
# ==========================================

selected_page = st.navigation(
    pages,
    position="hidden"
)

render_sidebar(pages)


# ==========================================
# DASHBOARD
# ==========================================

def render_dashboard():

    st.title("Marketing Intelligence")
    st.caption(
        "Monitor marketing data quality and operational health."
    )

    try:

        engine = get_connection()

        query = text("""
            SELECT *
            FROM vw_MarketingDataQuality
        """)

        metrics = pd.read_sql(query, engine).iloc[0]

        # Connection status
        st.success(
            "Connected to MarketingDataHealth database"
        )

        # ======================================
        # KEY PERFORMANCE INDICATORS
        # ======================================

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Records",
            f"{int(metrics['TotalRecords']):,}"
        )

        col2.metric(
            "Average Quality Score",
            f"{metrics['AverageQualityScore']:.2f}/100"
        )

        col3.metric(
            "Records Requiring Review",
            f"{int(metrics['RecordsRequiringReview']):,}"
        )

        review_percentage = (
            metrics["RecordsRequiringReview"]
            / metrics["TotalRecords"]
        ) * 100

        col4.metric(
            "Review Rate",
            f"{review_percentage:.1f}%"
        )

        st.divider()

        # ======================================
        # DATA COMPLETENESS
        # ======================================

        st.subheader("Data Completeness")

        completeness_data = pd.DataFrame({
            "Field": [
                "Company Name",
                "Email",
                "Job Title",
                "Campaign Name"
            ],
            "Missing Records": [
                metrics["MissingCompany"],
                metrics["MissingEmail"],
                metrics["MissingJobTitle"],
                metrics["MissingCampaign"]
            ]
        })

        fig = px.bar(
            completeness_data,
            x="Field",
            y="Missing Records",
            title="Missing Values by Field",
            text="Missing Records"
        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color="#172B4D",
            margin=dict(l=30, r=30, t=60, b=30)
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

        st.divider()

        # ======================================
        # DATA QUALITY ISSUES
        # ======================================

        st.subheader("Data Quality Issues")

        issue_data = pd.DataFrame({
            "Issue Type": [
                "Missing Company",
                "Missing Email",
                "Missing Job Title",
                "Missing Campaign",
                "Invalid Emails",
                "Duplicate Emails"
            ],
            "Records Affected": [
                metrics["MissingCompany"],
                metrics["MissingEmail"],
                metrics["MissingJobTitle"],
                metrics["MissingCampaign"],
                metrics["InvalidEmailRecords"],
                metrics["DuplicateEmailRecords"]
            ]
        })

        fig2 = px.bar(
            issue_data,
            x="Records Affected",
            y="Issue Type",
            orientation="h",
            title="Records Affected by Issue Type",
            text="Records Affected"
        )

        fig2.update_layout(
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color="#172B4D",
            margin=dict(l=30, r=30, t=60, b=30)
        )

        st.plotly_chart(
            fig2,
            width="stretch"
        )

    except Exception as e:

        st.error(
            f"Unable to load dashboard data: {e}"
        )


# ==========================================
# RUN SELECTED PAGE
# ==========================================

selected_page.run()
