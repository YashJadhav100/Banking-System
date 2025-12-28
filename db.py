import streamlit as st
import psycopg2

def get_connection():
    # If secrets are NOT present (GitHub / Streamlit Cloud)
    if "DB_HOST" not in st.secrets:
        return None

    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        port=st.secrets["DB_PORT"]
    )
