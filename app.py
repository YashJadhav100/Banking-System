import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from pdf_utils import generate_pdf
from datetime import datetime

st.set_page_config(page_title="ABC Bank", layout="centered")

# ------------------ DATABASE CONNECTION ------------------

def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        sslmode="require"
    )

# ------------------ DB HELPERS ------------------

def get_user(username):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE username=%s", (username,))
            return cur.fetchone()

def create_user(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING",
                (username,)
            )
            cur.execute(
                "INSERT INTO accounts (user_id) "
                "SELECT id FROM users WHERE username=%s "
                "ON CONFLICT DO NOTHING",
                (username,)
            )
            conn.commit()

def get_balance(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.balance FROM accounts a
                JOIN users u ON a.user_id=u.id
                WHERE u.username=%s
            """, (username,))
            return cur.fetchone()[0]

def log_transaction(sender, receiver, amount):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO transactions (sender, receiver, amount)
                VALUES (%s, %s, %s)
            """, (sender, receiver, amount))
            conn.commit()

def transfer_money(sender, receiver, amount):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE accounts SET balance = balance - %s
                WHERE user_id = (SELECT id FROM users WHERE username=%s)
            """, (amount, sender))

            cur.execute("""
                UPDATE accounts SET balance = balance + %s
                WHERE user_id = (SELECT id FROM users WHERE username=%s)
            """, (amount, receiver))

            conn.commit()

            log_transaction(sender, receiver, amount)

def get_transactions(username):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM transactions
                WHERE sender=%s OR receiver=%s
                ORDER BY created_at DESC
            """, (username, username))
            return cur.fetchall()

# ------------------ UI ------------------

st.title("🏦 ABC Bank")

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    username = st.text_input("Enter username")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            user = get_user(username)
            if user:
                st.session_state.user = username
                st.rerun()
            else:
                st.error("User not found")

    with col2:
        if st.button("Create Account"):
            create_user(username)
            st.success("Account created. You can login now.")

else:
    user = st.session_state.user
    st.success(f"Logged in as {user}")

    balance = get_balance(user)
    st.metric("Current Balance ($)", balance)

    st.subheader("💸 Send Money")
    receiver = st.text_input("Receiver username")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Send"):
        if receiver == user:
            st.error("Cannot send to yourself")
        else:
            transfer_money(user, receiver, amount)
            st.success("Transfer successful")
            st.rerun()

    st.subheader("📜 Transaction History")
    txns = get_transactions(user)
    st.table(txns)

    if st.button("📄 Download PDF Statement"):
        pdf = generate_pdf(user, txns)
        st.download_button("Download", pdf, file_name="statement.pdf")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
