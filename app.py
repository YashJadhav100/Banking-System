import streamlit as st
import psycopg2
from pdf_utils import generate_pdf
from datetime import datetime

# -----------------------------
# Database Connection
# -----------------------------
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=st.secrets["db"]["host"],
        port=st.secrets["db"]["port"],
        dbname=st.secrets["db"]["database"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"]
    )

conn = get_connection()
cur = conn.cursor()

# -----------------------------
# App UI
# -----------------------------
st.set_page_config(page_title="ABC Bank", layout="centered")
st.title("🏦 ABC Bank – Banking System MVP")

if "user" not in st.session_state:
    st.session_state.user = None

menu = ["Login", "Create User"]
choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------
# Create User
# -----------------------------
if choice == "Create User":
    st.subheader("Create New Account")

    username = st.text_input("Username")
    initial_balance = st.number_input("Initial Deposit", min_value=0.0, step=100.0)

    if st.button("Create Account"):
        cur.execute(
            "INSERT INTO users (username, balance) VALUES (%s, %s)",
            (username, initial_balance)
        )
        conn.commit()
        st.success("Account created successfully")

# -----------------------------
# Login
# -----------------------------
if choice == "Login":
    st.subheader("Login")

    username = st.text_input("Enter username")

    if st.button("Login"):
        cur.execute(
            "SELECT id, balance FROM users WHERE username=%s",
            (username,)
        )
        result = cur.fetchone()

        if result:
            st.session_state.user = {
                "id": result[0],
                "username": username,
                "balance": result[1]
            }
            st.success(f"Welcome {username}")
        else:
            st.error("User not found")

# -----------------------------
# Dashboard
# -----------------------------
if st.session_state.user:
    st.divider()
    st.subheader("Account Dashboard")

    st.write(f"**User:** {st.session_state.user['username']}")
    st.write(f"**Balance:** ${st.session_state.user['balance']}")

    amount = st.number_input("Amount", min_value=0.0, step=50.0)
    action = st.selectbox("Action", ["Deposit", "Withdraw"])

    if st.button("Submit"):
        if action == "Withdraw" and amount > st.session_state.user["balance"]:
            st.error("Insufficient balance")
        else:
            new_balance = (
                st.session_state.user["balance"] + amount
                if action == "Deposit"
                else st.session_state.user["balance"] - amount
            )

            cur.execute(
                "UPDATE users SET balance=%s WHERE id=%s",
                (new_balance, st.session_state.user["id"])
            )

            cur.execute(
                "INSERT INTO transactions (user_id, amount, type, timestamp) VALUES (%s, %s, %s, %s)",
                (
                    st.session_state.user["id"],
                    amount,
                    action,
                    datetime.now()
                )
            )

            conn.commit()
            st.session_state.user["balance"] = new_balance
            st.success("Transaction successful")

    # -----------------------------
    # Download Statement
    # -----------------------------
    if st.button("Download Statement (PDF)"):
        cur.execute(
            "SELECT amount, type, timestamp FROM transactions WHERE user_id=%s",
            (st.session_state.user["id"],)
        )
        transactions = cur.fetchall()

        pdf_bytes = generate_pdf(
            st.session_state.user["username"],
            transactions
        )

        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name="bank_statement.pdf",
            mime="application/pdf"
        )
