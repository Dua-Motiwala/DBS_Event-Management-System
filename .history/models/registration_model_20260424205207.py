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
    feedbackid = db.Column('FEEDBACKID', db.Integer, primary_key=True)
    userid = db.Column('USERID', db.Integer, db.ForeignKey('USERS.USERID'))
    eventid = db.Column('EVENTID', db.Integer, db.ForeignKey('EVENTS.EVENTID'))
    rating = db.Column('RATING', db.Integer) # 1-5
    feedbacktext = db.Column('FEEDBACKTEXT', db.String(255))

class AdminLog(db.Model):
    __tablename__ = 'ADMIN_LOG'
    logid = db.Column('LOGID', db.Integer, primary_key=True)
    userid = db.Column('USERID', db.Integer, db.ForeignKey('USERS.USERID'))
    action = db.Column('ACTION', db.String(255))
    actiontime = db.Column('ACTIONTIME', db.DateTime, default=datetime.utcnow)
