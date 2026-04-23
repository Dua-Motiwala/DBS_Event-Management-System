import oracledb

def get_connection():
    conn = oracledb.connect(
        user="Eent",          # your username
        password="YOUR_PASSWORD",
        dsn="localhost/XEPDB1"  # default for Oracle XE
    )
    return conn

