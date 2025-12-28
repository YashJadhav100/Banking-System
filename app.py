import streamlit as st
from db import get_connection
from pdf_utils import generate_statement
import pandas as pd

# -------------------------------------------------
# APP CONFIG
# -------------------------------------------------
st.set_page_config(page_title="ABC Bank", layout="centered")

# -------------------------------------------------
# SESSION SETUP
# -------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------------------------------
# DB CONNECTION
# -------------------------------------------------
conn = get_connection()
cur = conn.cursor()

st.title("🏦 ABC Bank")

# =================================================
# START SCREEN (LOGIN / CREATE USER)
# =================================================
if st.session_state.user is None:
    choice = st.radio("Choose an option", ["Login", "Create New User"])

    # ---------- LOGIN ----------
    if choice == "Login":
        username = st.text_input("Enter username")

        if st.button("Login"):
            cur.execute(
                "SELECT balance FROM users WHERE username = %s",
                (username,)
            )
            result = cur.fetchone()

            if result:
                st.session_state.user = username
                st.rerun()
            else:
                st.error("User not found")

    # ---------- CREATE USER ----------
    if choice == "Create New User":
        new_username = st.text_input("Choose a username")

        if st.button("Create Account"):
            try:
                cur.execute(
                    "INSERT INTO users (username, balance) VALUES (%s, %s)",
                    (new_username, 1000)
                )
                conn.commit()
                st.session_state.user = new_username
                st.success("Account created successfully!")
                st.rerun()
            except:
                st.error("Username already exists")

    st.stop()

# =================================================
# DASHBOARD
# =================================================
st.subheader(f"Welcome, {st.session_state.user} 👋")

cur.execute(
    "SELECT balance FROM users WHERE username = %s",
    (st.session_state.user,)
)
balance = cur.fetchone()[0]

st.metric("Current Balance", f"${balance}")

# =================================================
# SEND MONEY
# =================================================
st.divider()
st.subheader("💸 Send Money")

cur.execute(
    "SELECT username FROM users WHERE username != %s",
    (st.session_state.user,)
)
users = [row[0] for row in cur.fetchall()]

to_user = st.selectbox("Send to", users)
amount = st.number_input("Amount", min_value=1)

if st.button("Send Money"):
    if amount > balance:
        st.error("Insufficient balance")
    else:
        # Deduct from sender
        cur.execute(
            "UPDATE users SET balance = balance - %s WHERE username = %s",
            (amount, st.session_state.user)
        )
        # Add to receiver
        cur.execute(
            "UPDATE users SET balance = balance + %s WHERE username = %s",
            (amount, to_user)
        )
        # Log transaction
        cur.execute(
            """
            INSERT INTO transactions (from_user, to_user, amount)
            VALUES (%s, %s, %s)
            """,
            (st.session_state.user, to_user, amount)
        )
        conn.commit()
        st.success("Money sent successfully!")
        st.rerun()

# =================================================
# TRANSACTION HISTORY
# =================================================
st.divider()
st.subheader("📜 Transaction History")

df = pd.read_sql(
    """
    SELECT from_user, to_user, amount, timestamp
    FROM transactions
    WHERE from_user = %s OR to_user = %s
    ORDER BY timestamp DESC
    """,
    conn,
    params=(st.session_state.user, st.session_state.user)
)

st.dataframe(df, use_container_width=True)

# =================================================
# DOWNLOAD PDF STATEMENT
# =================================================
st.divider()
st.subheader("⬇️ Download Bank Statement (PDF)")

cur.execute(
    """
    SELECT from_user, to_user, amount, timestamp
    FROM transactions
    WHERE from_user = %s OR to_user = %s
    ORDER BY timestamp DESC
    """,
    (st.session_state.user, st.session_state.user)
)
transactions = cur.fetchall()

if transactions:
    pdf_file = generate_statement(st.session_state.user, transactions)

    st.download_button(
        label="Download Statement",
        data=pdf_file,
        file_name=f"{st.session_state.user}_statement.pdf",
        mime="application/pdf"
    )
else:
    st.info("No transactions yet")

# =================================================
# LOGOUT
# =================================================
st.divider()
if st.button("Logout"):
    st.session_state.user = None
    st.rerun()
