import oracledb

def get_connection():
    conn = oracledb.connect(
        user="EventDB",          # your username
        password="event123",
        dsn="localhost/xe"  # default for Oracle XE
    )
    return conn

