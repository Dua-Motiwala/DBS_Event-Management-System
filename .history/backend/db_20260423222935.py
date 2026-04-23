import oracledb

oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_12")

def get_connection():
    conn = oracledb.connect(
        user="event_user",
        password="event123",
        dsn="localhost/xe"
    )
    return conn