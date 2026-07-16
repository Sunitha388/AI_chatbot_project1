from database import get_connection


def get_chat_history(session_id, limit=5):
    conn = get_connection()
    if conn is None:
        return []   # no history available, but don't crash

    cursor = conn.cursor()
    query = """
    SELECT user_message, bot_response
    FROM chat_history
    WHERE session_id = %s
    ORDER BY id DESC
    LIMIT %s
    """
    cursor.execute(query, (session_id, limit))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows[::-1]