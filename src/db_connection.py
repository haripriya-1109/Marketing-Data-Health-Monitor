from sqlalchemy import create_engine
from urllib.parse import quote_plus
import streamlit as st


@st.cache_resource
def get_connection():

    server = r"localhost\SQLEXPRESS"
    database = "MarketingDataHealth"
    driver = "ODBC Driver 18 for SQL Server"

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    connection_url = (
        "mssql+pyodbc:///?odbc_connect="
        + quote_plus(connection_string)
    )

    return create_engine(connection_url)