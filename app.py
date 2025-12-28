import streamlit as st
from datetime import datetime
from pdf_utils import generate_pdf

st.set_page_config(page_title="ABC Bank", layout="centered")

# ------------------ INIT DATA ------------------
if "users" not in st.session_state:
    st.session_state.users = {
        "alice": {"balance": 1500, "txns": []},
        "bob": {"balance": 1200, "txns": []},
        "charlie": {"balance": 800, "txns": []},
    }

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ------------------ HEADER ------------------
st.title("🏦 ABC Bank")
st.caption("Banking System MVP (Streamlit Demo Version)")

# ------------------ AUTH ------------------
if st.session_state.current_user is None:
    choice = st.radio("Select Action", ["Login", "Create User"])

    username = st.text_input("Username").lower()

    if st.button(choice):
        if choice == "Login":
            if username in st.session_state.users:
                st.session_state.current_user = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("User not found")

        else:
            if username in st.session_state.users:
                st.error("User already exists")
            else:
                st.session_state.users[username] = {
                    "balance": 1000,
                    "txns": []
                }
                st.success("User created with $1000 balance")

    st.stop()

# ------------------ DASHBOARD ------------------
user = st.session_state.current_user
data = st.session_state.users[user]

st.subheader(f"Welcome, {user}")
st.metric("Current Balance", f"${data['balance']}")

st.divider()

# ------------------ SEND MONEY ------------------
st.subheader("💸 Send Money")

recipients = [u for u in st.session_state.users if u != user]
to_user = st.selectbox("Send to", recipients)
amount = st.number_input("Amount", min_value=1)

if st.button("Transfer"):
    if data["balance"] >= amount:
        data["balance"] -= amount
        st.session_state.users[to_user]["balance"] += amount

        txn = {
            "from": user,
            "to": to_user,
            "amount": amount,
            "time": datetime.now()
        }

        data["txns"].append(txn)
        st.session_state.users[to_user]["txns"].append(txn)

        st.success("Transfer successful")
        st.rerun()
    else:
        st.error("Insufficient balance")

st.divider()

# ------------------ TRANSACTIONS ------------------
st.subheader("📜 Transaction History")

if data["txns"]:
    st.table([
        {
            "From": t["from"],
            "To": t["to"],
            "Amount": f"${t['amount']}",
            "Time": t["time"].strftime("%Y-%m-%d %H:%M")
        } for t in data["txns"]
    ])

    pdf = generate_pdf(user, data["txns"])
    st.download_button(
        "📄 Download Statement (PDF)",
        pdf,
        file_name=f"{user}_statement.pdf"
    )
else:
    st.info("No transactions yet")

st.divider()

if st.button("Logout"):
    st.session_state.current_user = None
    st.rerun()
