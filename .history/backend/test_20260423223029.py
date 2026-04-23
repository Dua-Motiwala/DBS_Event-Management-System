from db import get_connection

conn = get_connection()
print("Database Connected Successfully!")
conn.close()python backend/test.py