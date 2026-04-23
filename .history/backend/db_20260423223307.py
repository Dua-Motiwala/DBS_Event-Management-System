import oracledb

def get_connection():
    conn = oracledb.connect(
        user="event_user",
        password="event123",
        dsn="localhost/xe"
    )
    return conn