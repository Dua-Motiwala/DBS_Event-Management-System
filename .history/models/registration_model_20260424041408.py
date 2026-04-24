from .user_model import db
from datetime import datetime

class Registration(db.Model):
    __tablename__ = 'REGISTRATIONS'
    regid = db.Column('REGID', db.Integer, primary_key=True)
    userid = db.Column('USERID', db.Integer, db.ForeignKey('USERS.USERID'))
    eventid = db.Column('EVENTID', db.Integer, db.ForeignKey('EVENTS.EVENTID'))
    regdate = db.Column('REGDATE', db.Date, default=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = 'PAYMENTS'


class Feedback(db.Model):
    __tablename__ = 'FEEDBACK'


class AdminLog(db.Model):
    __tablename__ = 'ADMIN_LOG'

