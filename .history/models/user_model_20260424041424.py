from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'USERS'
    
    userid = db.Column('USERID', db.Integer, primary_key=True)
    name = db.Column('NAME', db.String(100), nullable=False)
    email = db.Column('EMAIL', db.String(100), unique=True, nullable=False)
    password_hash = db.Column('PASSWORD', db.String(255), nullable=False)
    role = db.Column('ROLE', db.String(20), nullable=False) # Admin, Organizer, Attendee

    # Relationships
    events = db.relationship('Event', backref='organizer', lazy=True)
    registrations = db.relationship('Registration', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    logs = db.relationship('AdminLog', backref='admin', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.userid)
