from .user_model import db
from datetime import datetime

class Venue(db.Model):
    __tablename__ = 'VENUES'
    venueid = db.Column('VENUEID', db.Integer, primary_key=True)
    name = db.Column('NAME', db.String(100))
    location = db.Column('LOCATION', db.String(100))
    capacity = db.Column('CAPACITY', db.Integer)
    events = db.relationship('Event', backref='venue', lazy=True)

class Category(db.Model):
    __tablename__ = 'CATEGORIES'
    categoryid = db.Column('CATEGORYID', db.Integer, primary_key=True)
    categoryname = db.Column('CATEGORYNAME', db.String(100))
    events = db.relationship('Event', backref='category', lazy=True)
    
class Event(db.Model):
    __tablename__ = 'EVENTS'
    eventid = db.Column('EVENTID', db.Integer, primary_key=True)
    title = db.Column('TITLE', db.String(100))
    userid = db.Column('USERID', db.Integer, db.ForeignKey('USERS.USERID'))
    eventdate = db.Column('EVENTDATE', db.Date)
    venueid = db.Column('VENUEID', db.Integer, db.ForeignKey('VENUES.VENUEID'))
    categoryid = db.Column('CATEGORYID', db.Integer, db.ForeignKey('CATEGORIES.CATEGORYID'))
    registrations = db.relationship('Registration', backref='event', lazy=True)
    payments = db.relationship('Payment', backref='event', lazy=True)
    feedbacks = db.relationship('Feedback', backref='event', lazy=True)
    schedules = db.relationship('EventSchedule', backref='event', lazy=True)

class EventSchedule(db.Model):
    __tablename__ = 'EVENT_SCHEDULE'
    scheduleid = db.Column('SCHEDULEID', db.Integer, primary_key=True)
    eventid = db.Column('EVENTID', db.Integer, db.ForeignKey('EVENTS.EVENTID'))
    starttime = db.Column('STARTTIME', db.DateTime)   
    endtime = db.Column('ENDTIME', db.DateTime)
    