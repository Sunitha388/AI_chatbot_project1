from database import get_connection


def save_chat(session_id, user_message, bot_response):
    conn = get_connection()
    if conn is None:
        print("⚠️ Skipped saving chat — no DB connection")
        return

    cursor = conn.cursor()
    query = """
    INSERT INTO chat_history
    (session_id, user_message, bot_response)
    VALUES (%s,%s,%s)
    """
    cursor.execute(query, (session_id, user_message, bot_response))
    conn.commit()
    cursor.close()
    conn.close()