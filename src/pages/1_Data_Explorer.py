
import streamlit as st
import pandas as pd
from db_connection import get_connection
from styles import apply_custom_styles


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Data Explorer",
    page_icon="🔎",
    layout="wide"
)

apply_custom_styles()


# ==========================================
# PAGE HEADER
# ==========================================

st.title("Marketing Data Explorer")

st.caption(
    "Search, explore, and filter marketing records "
    "across your dataset."
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    engine = get_connection()

    query = """
        SELECT *
        FROM MarketingLeads
    """

    return pd.read_sql(query, engine)


try:

    df = load_data()

    # ==========================================
    # DATASET SUMMARY
    # ==========================================

    st.metric(
        "Total Marketing Records",
        f"{len(df):,}"
    )

    st.divider()


    # ==========================================
    # SEARCH
    # ==========================================

    st.subheader("Find Marketing Records")

    search_term = st.text_input(
        "Search by company name or email",
        placeholder="Enter a company name or email address..."
    )

    filtered_df = df.copy()

    if search_term:

        filtered_df = filtered_df[
            filtered_df["company_name"].str.contains(
                search_term,
                case=False,
                na=False
            )
            |
            filtered_df["email"].str.contains(
                search_term,
                case=False,
                na=False
            )
        ]


    # ==========================================
    # FILTERS
    # ==========================================

    col1, col2, col3 = st.columns(3)

    with col1:

        regions = st.multiselect(
            "Region",
            options=sorted(df["region"].dropna().unique()),
            placeholder="All regions"
        )

    with col2:

        sources = st.multiselect(
            "Lead Source",
            options=sorted(df["lead_source"].dropna().unique()),
            placeholder="All sources"
        )

    with col3:

        stages = st.multiselect(
            "Lifecycle Stage",
            options=sorted(df["lifecycle_stage"].dropna().unique()),
            placeholder="All stages"
        )


    if regions:
        filtered_df = filtered_df[
            filtered_df["region"].isin(regions)
        ]

    if sources:
        filtered_df = filtered_df[
            filtered_df["lead_source"].isin(sources)
        ]

    if stages:
        filtered_df = filtered_df[
            filtered_df["lifecycle_stage"].isin(stages)
        ]


    # ==========================================
    # RESULTS
    # ==========================================

    st.divider()

    result_col1, result_col2 = st.columns([3, 1])

    with result_col1:
        st.subheader("Marketing Records")

    with result_col2:
        st.metric(
            "Matching Records",
            f"{len(filtered_df):,}"
        )


    # ==========================================
    # TABLE DISPLAY
    # ==========================================

    display_columns = [
        "record_id",
        "company_name",
        "first_name",
        "last_name",
        "email",
        "job_title",
        "lead_source",
        "region",
        "lifecycle_stage",
        "consent_status"
    ]

    available_columns = [
        column for column in display_columns
        if column in filtered_df.columns
    ]

    display_df = filtered_df[available_columns].copy()

    display_df = display_df.fillna("Not provided")

    
    if not display_df.empty:

        table_height = min(
            480,
            max(100, 38 * len(display_df) + 38)
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=table_height,
            column_config={
                "record_id": st.column_config.TextColumn(
                    "Record ID",
                    width="medium"
                ),
                "company_name": st.column_config.TextColumn(
                    "Company",
                    width="medium"
                ),
                "first_name": st.column_config.TextColumn(
                    "First Name",
                    width="small"
                ),
                "last_name": st.column_config.TextColumn(
                    "Last Name",
                    width="small"
                ),
                "email": st.column_config.TextColumn(
                    "Email",
                    width="large"
                ),
                "job_title": st.column_config.TextColumn(
                    "Job Title",
                    width="medium"
                ),
                "lead_source": st.column_config.TextColumn(
                    "Lead Source",
                    width="medium"
                ),
                "region": st.column_config.TextColumn(
                    "Region",
                    width="medium"
                ),
                "lifecycle_stage": st.column_config.TextColumn(
                    "Lifecycle Stage",
                    width="medium"
                ),
                "consent_status": st.column_config.TextColumn(
                    "Consent Status",
                    width="medium"
                )
            }
        )

    else:

        st.info(
            "No marketing records match your search or filters. "
            "Try adjusting your selection."
        )


except Exception as e:

    st.error(f"Unable to load marketing records: {e}")
    st.exception(e)
