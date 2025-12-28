import streamlit as st
import psycopg2
from contextlib import contextmanager
from pdf_utils import generate_pdf
from datetime import datetime

st.set_page_config(page_title="ABC Bank", page_icon="🏦", layout="centered")


@contextmanager
def get_connection():
    conn = psycopg2.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        sslmode="require"
    )
    try:
        yield conn
    finally:
        conn.close()


def get_user(username):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, balance FROM users WHERE username=%s", (username,))
        return cur.fetchone()


def create_user(username):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, balance) VALUES (%s, %s) RETURNING id",
            (username, 1000)
        )
        conn.commit()
        return cur.fetchone()[0]


def log_transaction(user_id, txn_type, amount):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO transactions (user_id, type, amount, created_at) VALUES (%s,%s,%s,%s)",
            (user_id, txn_type, amount, datetime.now())
        )
        conn.commit()


def update_balance(user_id, amount):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET balance = balance + %s WHERE id=%s",
            (amount, user_id)
        )
        conn.commit()


def get_statement(user_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT type, amount, created_at FROM transactions WHERE user_id=%s ORDER BY created_at DESC",
            (user_id,)
        )
        return cur.fetchall()


# ---------------- UI ---------------- #

st.title("🏦 ABC Bank")

if "user" not in st.session_state:
    st.session_state.user = None

choice = st.radio("Choose an option", ["Login", "Create Account"])

username = st.text_input("Enter username")

if choice == "Create Account" and st.button("Create"):
    if get_user(username):
        st.error("User already exists")
    else:
        create_user(username)
        st.success("Account created with $1000 balance")

if choice == "Login" and st.button("Login"):
    user = get_user(username)
    if user:
        st.session_state.user = (user[0], username, user[1])
    else:
        st.error("User not found")

if st.session_state.user:
    user_id, uname, balance = st.session_state.user
    st.success(f"Welcome {uname}")
    st.metric("Balance", f"${balance}")

    amount = st.number_input("Amount", min_value=1)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Deposit"):
            update_balance(user_id, amount)
            log_transaction(user_id, "DEPOSIT", amount)
            st.experimental_rerun()

    with col2:
        if st.button("Withdraw"):
            if amount > balance:
                st.error("Insufficient balance")
            else:
                update_balance(user_id, -amount)
                log_transaction(user_id, "WITHDRAW", amount)
                st.experimental_rerun()

    if st.button("Download Statement (PDF)"):
        txns = get_statement(user_id)
        pdf = generate_pdf(uname, txns)
        st.download_button(
            "Download PDF",
            pdf,
            file_name="statement.pdf",
            mime="application/pdf"
        )
