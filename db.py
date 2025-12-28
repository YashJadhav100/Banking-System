import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="banking_db",
        user="postgres",
        password="YASH"
    )
