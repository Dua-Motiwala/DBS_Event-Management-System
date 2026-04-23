import os

class Config:
    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key-12345'
    
    # Oracle Database Settings
    # Format: oracle+oracledb://user:password@host:port/?service_name=service_name
    # Or: oracle+oracledb://user:password@dsn
    DB_USER = "event_user"  # Change to your Oracle username
    DB_PASSWORD = "event123"  # Change to your Oracle password
    DB_HOST = "localhost"
    DB_PORT = "1521"
    DB_SERVICE = "xe"  # Standard for Oracle XE
    
    SQLALCHEMY_DATABASE_URI = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload Settings
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
