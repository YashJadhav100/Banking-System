import streamlit as st
import psycopg2
from pdf_utils import generate_pdf
from datetime import datetime

# -----------------------------
# Database connection (Supabase)
# -----------------------------
def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        port=st.secrets["DB_PORT"]
    )

st.set_page_config(page_title="ABC Bank", layout="wide")

st.title("🏦 ABC Bank – Banking System MVP")

# -----------------------------
# Login (simple username)
# -----------------------------
username = st.text_input("Enter your username")

if not username:
    st.stop()

conn = get_connection()
cur = conn.cursor()

# Ensure user exists
cur.execute("""
    INSERT INTO users (username, balance)
    VALUES (%s, 1000)
    ON CONFLICT (username) DO NOTHING
""", (username,))
conn.commit()

# -----------------------------
# Fetch balance
# -----------------------------
cur.execute("SELECT balance FROM users WHERE username=%s", (username,))
balance = cur.fetchone()[0]

st.metric("💰 Current Balance", f"${balance:.2f}")

# -----------------------------
# Send money
# -----------------------------
st.subheader("💸 Send Money")

to_user = st.text_input("Send to user")
amount = st.number_input("Amount", min_value=1.0, step=1.0)

if st.button("Send"):
    cur.execute("SELECT balance FROM users WHERE username=%s", (username,))
    sender_balance = cur.fetchone()[0]

    if sender_balance < amount:
        st.error("Insufficient balance")
    else:
        cur.execute("""
            INSERT INTO users (username, balance)
            VALUES (%s, 1000)
            ON CONFLICT (username) DO NOTHING
        """, (to_user,))

        cur.execute(
            "UPDATE users SET balance = balance - %s WHERE username=%s",
            (amount, username)
        )
        cur.execute(
            "UPDATE users SET balance = balance + %s WHERE username=%s",
            (amount, to_user)
        )

        cur.execute("""
            INSERT INTO transactions (from_user, to_user, amount, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (username, to_user, amount, datetime.utcnow()))

        conn.commit()
        st.success("Transfer successful 🎉")
        st.experimental_rerun()

# -----------------------------
# Transaction history
# -----------------------------
st.subheader("📜 Transaction History")

cur.execute("""
    SELECT from_user, to_user, amount, timestamp
    FROM transactions
    WHERE from_user=%s OR to_user=%s
    ORDER BY timestamp DESC
""", (username, username))

transactions = cur.fetchall()

st.table(transactions)

# -----------------------------
# Download PDF statement
# -----------------------------
if st.button("📄 Download Statement (PDF)"):
    pdf_bytes = generate_pdf(username, transactions)
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=f"{username}_statement.pdf",
        mime="application/pdf"
    )

cur.close()
conn.close()
