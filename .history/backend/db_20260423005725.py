import oracledb

def get_connection():
    conn = oracledb.connect(
        user="system",          # your username
        password="YOUR_PASSWORD",
        dsn="localhost/XEPDB1"  # default for Oracle XE
    )
    return conn

