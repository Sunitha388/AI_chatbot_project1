from database import get_connection

conn = get_connection()

if conn:
    print("✅ Database connection is working!")
    conn.close()
else:
    print("❌ Database connection failed!")
    
    
    
    
    