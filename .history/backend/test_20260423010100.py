from db import get_connection

conn = get_connection()
print("Connected to Oracle successfully!")
conn.close()