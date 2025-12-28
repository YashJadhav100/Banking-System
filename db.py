import psycopg2

def get_connection():
    try:
        return psycopg2.connect(
            host="localhost",
            database="banking_db",
            user="postgres",
            password="YASH",  # local only
            port="5432"
        )
    except Exception:
        # Cloud / demo mode fallback
        return None
