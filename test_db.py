from database import get_connection

conn = get_connection()
if conn:
    print("Connection object:", conn)
    conn.close()
else:
    print("Connection failed.")