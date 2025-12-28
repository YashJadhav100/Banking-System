import streamlit as st
import sqlite3
from datetime import datetime

# ---------------- DATABASE ---------------- #
def get_connection():
    return sqlite3.connect("bank.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        balance INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        amount INTEGER,
        timestamp TEXT
    )
    """)

    # Pre-existing users
    predefined_users = {
        "alice": 5000,
        "bob": 5000,
        "charlie": 5000
    }

    for user, balance in predefined_users.items():
        cur.execute(
            "INSERT OR IGNORE INTO users (username, balance) VALUES (?, ?)",
            (user, balance)
        )

    conn.commit()
    conn.close()

# ---------------- USER FUNCTIONS ---------------- #
def create_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?)", (username, 100))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()
    return user

def update_balance(username, amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET balance = balance + ? WHERE username=?",
        (amount, username)
    )
    conn.commit()
    conn.close()

def log_transaction(sender, receiver, amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (sender, receiver, amount, timestamp) VALUES (?, ?, ?, ?)",
        (sender, receiver, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_transactions(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT sender, receiver, amount, timestamp 
        FROM transactions 
        WHERE sender=? OR receiver=?
        ORDER BY timestamp DESC
    """, (username, username))
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------------- APP START ---------------- #
st.set_page_config(page_title="ABC Bank", layout="centered")
init_db()

st.title("🏦 ABC Bank")

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN / REGISTER ---------------- #
if not st.session_state.user:
    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Create Account"])

    with tab1:
        username = st.text_input("Username")
        if st.button("Login"):
            user = get_user(username)
            if user:
                st.session_state.user = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("User not found")

    with tab2:
        new_user = st.text_input("Choose Username")
        if st.button("Create Account"):
            if get_user(new_user):
                st.error("User already exists")
            else:
                create_user(new_user)
                st.success("Account created with ₹100 balance")

    st.markdown("### 🧪 Demo Users")
    st.write("You can login using:")
    st.code("alice\nbob\ncharlie")

# ---------------- DASHBOARD ---------------- #
else:
    user = get_user(st.session_state.user)
    st.subheader(f"Welcome, {st.session_state.user}")

    st.metric("💰 Balance", f"₹{user[1]}")

    # SEND MONEY
    st.markdown("### 💸 Send Money")
    receiver = st.text_input("Send to")
    amount = st.number_input("Amount", min_value=1, step=1)

    if st.button("Send"):
        receiver_user = get_user(receiver)
        if not receiver_user:
            st.error("Receiver does not exist")
        elif amount > user[1]:
            st.error("Insufficient balance")
        else:
            update_balance(st.session_state.user, -amount)
            update_balance(receiver, amount)
            log_transaction(st.session_state.user, receiver, amount)
            st.success("Transfer successful")
            st.rerun()

    # TRANSACTION HISTORY
    st.markdown("### 📜 Transaction History")
    transactions = get_transactions(st.session_state.user)

    if transactions:
        for t in transactions:
            direction = "Sent" if t[0] == st.session_state.user else "Received"
            st.write(f"{direction} ₹{t[2]} | {t[3]} | {t[0]} → {t[1]}")
    else:
        st.info("No transactions yet")

    # LOGOUT
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
