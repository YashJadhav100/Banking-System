import streamlit as st
from supabase import create_client

# ---------------- CONFIG ----------------
st.set_page_config(page_title="ABC Bank", layout="centered")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- DB HELPERS ----------------
def get_user(username):
    res = supabase.table("users").select("*").eq("username", username).execute()
    return res.data[0] if res.data else None

def create_user(username):
    supabase.table("users").insert({
        "username": username,
        "balance": 1000
    }).execute()

def update_balance(username, new_balance):
    supabase.table("users").update({
        "balance": new_balance
    }).eq("username", username).execute()

def log_transaction(sender, receiver, amount):
    supabase.table("transactions").insert({
        "sender": sender,
        "receiver": receiver,
        "amount": amount
    }).execute()

def get_transactions(username):
    res = supabase.table("transactions") \
        .select("*") \
        .or_(f"sender.eq.{username},receiver.eq.{username}") \
        .order("created_at", desc=True) \
        .execute()
    return res.data

# ---------------- UI ----------------
st.title("🏦 ABC Bank")

if "user" not in st.session_state:
    st.session_state.user = None

menu = ["Login", "Create User"]
choice = st.sidebar.selectbox("Menu", menu)

# -------- LOGIN --------
if choice == "Login":
    username = st.text_input("Enter username")

    if st.button("Login"):
        user = get_user(username)
        if user:
            st.session_state.user = user
            st.success(f"Welcome back, {username}")
        else:
            st.error("User not found")

# -------- CREATE USER --------
if choice == "Create User":
    username = st.text_input("New username")

    if st.button("Create"):
        if get_user(username):
            st.error("User already exists")
        else:
            create_user(username)
            st.success("User created with ₹1000 balance")

# -------- DASHBOARD --------
if st.session_state.user:
    user = get_user(st.session_state.user["username"])
    st.divider()

    st.subheader(f"👤 {user['username']}")
    st.metric("Balance", f"₹ {user['balance']}")

    # SEND MONEY
    st.subheader("💸 Send Money")
    to_user = st.text_input("Send to")
    amount = st.number_input("Amount", min_value=1, step=1)

    if st.button("Send"):
        receiver = get_user(to_user)
        if not receiver:
            st.error("Receiver not found")
        elif amount > user["balance"]:
            st.error("Insufficient balance")
        else:
            update_balance(user["username"], user["balance"] - amount)
            update_balance(to_user, receiver["balance"] + amount)
            log_transaction(user["username"], to_user, amount)
            st.success("Transfer successful")
            st.experimental_rerun()

    # TRANSACTIONS
    st.subheader("📄 Transactions")
    txns = get_transactions(user["username"])

    if txns:
        for t in txns:
            direction = "⬅️ Received" if t["receiver"] == user["username"] else "➡️ Sent"
            st.write(f"{direction} ₹{t['amount']} | {t['created_at']}")
    else:
        st.info("No transactions yet")

    if st.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()
