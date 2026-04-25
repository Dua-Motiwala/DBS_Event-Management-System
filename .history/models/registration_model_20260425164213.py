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
    paymentid = db.Column('PAYMENTID', db.Integer, primary_key=True)
    paymentstatus = db.Column('PAYMENTSTATUS', db.String(20))
    eventid = db.Column('EVENTID', db.Integer, db.ForeignKey('EVENTS.EVENTID'))
    amount = db.Column('AMOUNT', db.Numeric(10, 2))
    userid = db.Column('USERID', db.Integer, db.ForeignKey('USERS.USERID'))
 
class Feedback(db.Model):
    __tablename__ = 'FEEDBACK'
    feedbackid = db.Column('FEEDBACKID', db.Integer, primary_key=True)
    userid = db.Column('USERID', db.Integer, db.ForeignKey('USERS.USERID'))
    eventid = db.Column('EVENTID', db.Integer, db.ForeignKey('EVENTS.EVENTID'))
    rating = db.Column('RATING', db.Integer) # 1-5
    feedbacktext = db.Column('FEEDBACKTEXT', db.String(20))

class AdminLog(db.Model):
    __tablename__ = 'ADMIN_LOG'
    logid = db.Column('ADMIN_LOG', db.Integer, primary_key=True)
    userid = db.Column('USERID', db.Integer, db.ForeignKey('USERS.USERID'))
    actiontime = db.Column('ADMIN_LOG', db.DateTime, default=datetime.utcnow)
    action = db.Column('ADMIN_LOG', db.String(20))
    