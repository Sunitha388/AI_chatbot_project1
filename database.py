import mysql.connector
from config import DB_CONFIG


def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            ssl_disabled=False,
            connect_timeout=10   # fail fast instead of hanging
        )
        print("✅ Database Connected Successfully")
        return conn

    except Exception as e:
        print("❌ Database Connection Error")
        print(e)
        return None