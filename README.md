# 🏦 ABC Bank – Banking System MVP

A full-stack **Banking System MVP** built using **Python, Streamlit, and PostgreSQL** that simulates real-world banking operations including user creation, authentication, money transfers, balance tracking, transaction history, and downloadable PDF bank statements.

This project demonstrates **end-to-end application development**, database integration, and clean system design suitable for academic, portfolio, and interview use.

## 🚀 Features

* 🔐 **User Authentication**

  * Login existing users
  * Create new bank accounts

* 💰 **Account Management**

  * View real-time account balance
  * Receive and send money between users

* 🔁 **Money Transfer System**

  * Transfer funds to any existing user
  * Automatic balance updates for sender and receiver
  * Transaction logging with timestamps

* 📄 **PDF Bank Statements**

  * Download transaction history as a professionally formatted PDF
  * Includes sender, receiver, amount, and date

* 🧪 **Pre-Seeded Users**

  * Comes with pre-created demo users (`alice`, `bob`, `charlie`) with initial balances for testing

---

## 🛠️ Tech Stack

| Layer           | Technology   |
| --------------- | ------------ |
| Frontend        | Streamlit    |
| Backend         | Python       |
| Database        | PostgreSQL   |
| PDF Reports     | ReportLab    |
| DB Driver       | psycopg2     |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```
Banking-System/
│
├── app.py              # Streamlit UI & application logic
├── db.py               # Database connection & queries
├── schema.sql          # SQL schema + seed data
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

## 🗄️ Database Schema

The database includes:

* `users` table
* `transactions` table

All tables and seed users are defined in `schema.sql`.

⚠️ **Note:** The actual database is **not uploaded**.

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YashJadhav100/Banking-System.git
cd Banking-System
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Setup PostgreSQL

* Create a PostgreSQL database (e.g. `banking_db`)
* Run `schema.sql` in pgAdmin or psql to create tables and seed users

### 4️⃣ Configure Database Connection

Update credentials inside `db.py`:

```python
dbname="banking_db"
user="postgres"
password="your_password"
host="localhost"
port="5432"
```

### 5️⃣ Run the Application

```bash
python -m streamlit run app.py
```

The app will be available at:

```

```

## 🧑‍💻 Sample Users (Preloaded)

| Username | Initial Balance |
| -------- | --------------- |
| alice    | $5000           |
| bob      | $5000           |
| charlie  | $5000           |

You can also create new users directly from the UI.


## 🎯 Learning Outcomes

This project demonstrates:

* Full-stack application design
* Relational database modeling
* Secure transaction handling
* Real-time UI updates
* PDF generation from database records
* Clean separation of concerns (UI vs DB logic)

## 📌 Future Improvements

* Password-based authentication
* Transaction notifications
* Deployment on Streamlit Cloud
* Role-based access control
* API-based backend (FastAPI)

## 👤 Author

**Yash Jadhav**
Graduate Student – Computer Science
📍 Syracuse University
🔗 [GitHub](https://github.com/YashJadhav100)
🔗 [LinkedIn](https://www.linkedin.com/in/yashvjadhav)
