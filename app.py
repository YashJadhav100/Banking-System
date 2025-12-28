import streamlit as st
from db import get_connection
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

st.set_page_config(page_title="ABC Bank", layout="centered")

# ---------- DB CONNECTION ----------
conn = get_connection()
demo_mode = conn is None

# ---------- DEMO DATA ----------
DEMO_USERS = {
    "alice": 5000,
    "bob": 5000,
    "charlie": 5000
}

DEMO_TRANSACTIONS = []

# ---------- HELPERS ----------
def fetch_users():
    if demo_mode:
        return list(DEMO_USERS.keys())
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")
    users = [row[0] for row in cur.fetchall()]
    cur.close()
    return users

def get_balance(username):
    if demo_mode:
        return DEMO_USERS.get(username, 0)
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE username=%s", (username,))
    res = cur.fetchone()
    cur.close()
    return res[0] if res else 0

def send_money(sender, receiver, amount):
    if demo_mode:
        DEMO_USERS[sender] -= amount
        DEMO_USERS[receiver] += amount
        DEMO_TRANSACTIONS.append(
            (sender, receiver, amount, datetime.now())
        )
        return

    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = balance - %s WHERE username=%s", (amount, sender))
    cur.execute("UPDATE users SET balance = balance + %s WHERE username=%s", (amount, receiver))
    cur.execute(
        "INSERT INTO transactions (from_user, to_user, amount) VALUES (%s,%s,%s)",
        (sender, receiver, amount)
    )
    conn.commit()
    cur.close()

def fetch_transactions(username):
    if demo_mode:
        return [t for t in DEMO_TRANSACTIONS if t[0] == username or t[1] == username]

    cur = conn.cursor()
    cur.execute("""
        SELECT from_user, to_user, amount, timestamp
        FROM transactions
        WHERE from_user=%s OR to_user=%s
        ORDER BY timestamp DESC
    """, (username, username))
    rows = cur.fetchall()
    cur.close()
    return rows

def generate_pdf(username, transactions):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf = canvas.Canvas(tmp.name, pagesize=letter)
    pdf.setFont("Helvetica", 10)

    pdf.drawString(50, 750, f"ABC Bank - Statement for {username}")
    y = 720

    for t in transactions:
        pdf.drawString(50, y, f"{t[3]} | {t[0]} → {t[1]} | ${t[2]}")
        y -= 20
        if y < 50:
            pdf.showPage()
            y = 750

    pdf.save()
    return tmp.name

# ---------- UI ----------
st.title("🏦 ABC Bank")

if demo_mode:
    st.warning("Running in demo mode (database not connected).")

auth_option = st.radio("Choose action", ["Login", "Create User"])

if auth_option == "Create User":
    new_user = st.text_input("Choose username")
    if st.button("Create"):
        if demo_mode:
            DEMO_USERS[new_user] = 1000
            st.success("User created (demo)")
        else:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, balance) VALUES (%s, 1000)", (new_user,))
            conn.commit()
            cur.close()
            st.success("User created")

else:
    username = st.text_input("Enter username")
    if st.button("Login"):
        users = fetch_users()
        if username not in users:
            st.error("User not found")
            st.stop()

        balance = get_balance(username)
        st.success(f"Welcome {username}")
        st.metric("Balance", f"${balance}")

        st.divider()
        st.subheader("💸 Send Money")

        receivers = [u for u in fetch_users() if u != username]
        to_user = st.selectbox("Send to", receivers)
        amount = st.number_input("Amount", min_value=1)

        if st.button("Send"):
            if amount > balance:
                st.error("Insufficient balance")
            else:
                send_money(username, to_user, amount)
                st.success("Transaction successful")

        st.divider()
        st.subheader("📜 Transaction History")

        txns = fetch_transactions(username)
        if txns:
            for t in txns:
                st.write(f"{t[3]} | {t[0]} → {t[1]} | ${t[2]}")
        else:
            st.info("No transactions")

        if st.button("📄 Download PDF Statement"):
            pdf_path = generate_pdf(username, txns)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download Statement",
                    data=f,
                    file_name="statement.pdf",
                    mime="application/pdf"
                )
