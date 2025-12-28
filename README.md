# 🏦 Banking System (Streamlit App)

A feature-complete **Banking System MVP** built using **Python + Streamlit**, supporting core banking operations such as user login, fund transfers, balance checks, transaction history, and PDF statement downloads.

This project intentionally demonstrates **two database implementations** to reflect real-world development and deployment constraints.

## 🚀 Features

* User login and account access
* Pre-loaded demo users (`alice`, `bob`, `charlie`)
* Send and receive money between users
* Real-time balance updates
* Transaction history tracking
* Downloadable bank statement (PDF)
* Modular backend design

## 🧱 Project Structure

```
Banking-System/
│
├── app.py          # PostgreSQL-based implementation (local development)
├── app1.py         # SQLite-based implementation (deployment-friendly)
├── db.py           # Database helper functions (PostgreSQL)
├── pdf_utils.py    # PDF statement generation
├── schema.sql      # PostgreSQL database schema
├── requirements.txt
├── README.md
```

## 🗄️ Database Implementations (Important)

This project contains **two working database approaches**, each used for a specific purpose.

## 🔹 1. PostgreSQL Version (Host Machine / Local Development)

**Files involved:**

* `app.py`
* `db.py`
* `schema.sql`

### How this version works:

* Uses **PostgreSQL** installed on the host machine
* Database schema is defined in `schema.sql`
* Credentials are configured locally
* Full relational database behavior is supported

### Why this version exists:

* Represents a **proper backend architecture**
* Shows experience with:

  * Relational databases
  * SQL schema design
  * Persistent data storage
* Suitable for:

  * Local development
  * Academic projects
  * Backend system design demonstrations

⚠️ **Note:**
This version is **not deployed publicly**, as Streamlit Cloud does not support external database services directly.

## 🔹 2. SQLite Version (Streamlit Cloud / Public Deployment)

**File involved:**

* `app1.py`

### Why SQLite was used:

* Streamlit Cloud does **not allow uploading or managing external databases**
* Environment variables and persistent DB services are restricted
* SQLite allows the app to run **out-of-the-box** for any viewer

### How this version works:

* Uses **SQLite** as an embedded database
* Database and tables are created automatically at runtime
* Demo users (`alice`, `bob`, `charlie`) are inserted programmatically
* All banking features remain identical to the PostgreSQL version

### This is the version used for:

* GitHub hosting
* Streamlit Cloud deployment
* Public demos and portfolio viewing

## 🔄 Why Two Versions?

This dual-approach reflects **real-world engineering trade-offs**:

| Environment               | Database   |
| ------------------------- | ---------- |
| Local / Host Machine      | PostgreSQL |
| Cloud / Public Deployment | SQLite     |

Instead of removing PostgreSQL, the project **adapts** to deployment constraints while preserving backend design integrity.

This demonstrates:

* Practical problem solving
* Deployment awareness
* Production-safe decision making

## ▶️ How to Run

### Run SQLite Version (Recommended for GitHub / Streamlit)

```bash
streamlit run app1.py
```

No setup required.


### Run PostgreSQL Version (Local Machine Only)

1. Install PostgreSQL
2. Create database using `schema.sql`
3. Configure credentials in `db.py`
4. Run:

```bash
streamlit run app.py
```

## 📄 PDF Statements

Users can download their transaction history as a **PDF bank statement**, generated using `pdf_utils.py`.

## 🧠 Key Takeaways

* Demonstrates backend + frontend integration
* Shows adaptability across environments
* Clean separation of concerns
* Production-aware architecture choices
