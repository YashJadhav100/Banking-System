## 🏦 Banking System – Database Implementation Details

This project was implemented using **two different database approaches**, depending on the execution environment. Both approaches are included in the repository to demonstrate **development vs deployment practices**.

## 🔹 1. Host Machine (Local Development – PostgreSQL)

During development on the host machine (local system), the banking system was built using **PostgreSQL**.

### What was done locally:

* PostgreSQL was installed and configured on the host machine
* A relational schema was created for:

  * Users
  * Account balances
  * Transaction history
* All banking operations were implemented using PostgreSQL queries:

  * Create user
  * Login
  * Send money
  * Receive money
  * Check balance
  * View transaction statements
* Three demo users were created locally:

  * `alice`
  * `bob`
  * `charlie`

### Files related to local PostgreSQL setup:

```
schema.sql
db.py
app.py
```

This version works correctly **only on the host machine**, as it depends on:

* A running PostgreSQL service
* Local database credentials
* Network access to the database

## 🔹 2. Deployment Version (Streamlit Cloud – SQLite)

For deployment and public access, the application was **refactored to use SQLite**.

### Why this change was required:

* Streamlit Cloud does not support persistent external databases
* Database credentials and services cannot be bundled with the app
* The project needs to run instantly for anyone viewing it online

### What was done for deployment:

* SQLite was used as an embedded database
* The database is created automatically at runtime
* Tables are initialized programmatically
* Demo users (`alice`, `bob`, `charlie`) are inserted automatically if they do not exist
* All banking features remain **identical** to the PostgreSQL version

### Features supported in the deployed version:

* Login
* Send money
* Receive money
* Check balance
* Transaction history
* Preloaded demo users

No external setup or database upload is required.

## ✅ Final Setup Used in This Repository

| Environment                      | Database   |
| -------------------------------- | ---------- |
| Host machine (local development) | PostgreSQL |
| Streamlit Cloud (deployment)     | SQLite     |

Both implementations are intentionally included to show:

* Proper backend database design (PostgreSQL)
* Practical cloud deployment adaptation (SQLite)
* Real-world engineering decision-making

## 📌 Note

Since Streamlit Cloud does not allow uploading or managing external databases, the **SQLite-based implementation is used for the live deployed app**, while the **PostgreSQL implementation reflects the original full backend design used during development**.
