import streamlit as st
import psycopg2
from pdf_utils import generate_pdf
from datetime import datetime

st.set_page_config(page_title="ABC Bank", layout="centered")

# ---------- DB CONNECTION ----------
def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        port=int(st.secrets["DB_PORT"])  # CRITICAL FIX
    )

# ---------- UI ----------
st.title("🏦 ABC Bank")

username = st.text_input("Enter username")

if username:
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Check user
        cur.execute("SELECT balance FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if not user:
            st.error("User not found")
        else:
            balance = user[0]
            st.success(f"Welcome {username}")
            st.metric("Balance", f"${balance}")

            # SEND MONEY
            st.subheader("💸 Send Money")
            cur.execute("SELECT username FROM users WHERE username != %s", (username,))
            users = [u[0] for u in cur.fetchall()]
            recipient = st.selectbox("Send to", users)
            amount = st.number_input("Amount", min_value=1)

            if st.button("Send"):
                cur.execute(
                    "UPDATE users SET balance = balance - %s WHERE username = %s",
                    (amount, username)
                )
                cur.execute(
                    "UPDATE users SET balance = balance + %s WHERE username = %s",
                    (amount, recipient)
                )
                cur.execute(
                    "INSERT INTO transactions (from_user, to_user, amount, timestamp) VALUES (%s,%s,%s,%s)",
                    (username, recipient, amount, datetime.now())
                )
                conn.commit()
                st.success("Transfer successful")
                st.experimental_rerun()

            # TRANSACTIONS
            st.subheader("📜 Transaction History")
            cur.execute("""
                SELECT from_user, to_user, amount, timestamp
                FROM transactions
                WHERE from_user = %s OR to_user = %s
                ORDER BY timestamp DESC
            """, (username, username))
            txns = cur.fetchall()

            if txns:
                st.table(txns)

                if st.button("📄 Download Statement PDF"):
                    pdf = generate_pdf(username, txns)
                    st.download_button(
                        "Download PDF",
                        pdf,
                        file_name=f"{username}_statement.pdf",
                        mime="application/pdf"
                    )

        cur.close()
        conn.close()

    except Exception as e:
        st.error("Database connection error. Check Streamlit secrets.")
