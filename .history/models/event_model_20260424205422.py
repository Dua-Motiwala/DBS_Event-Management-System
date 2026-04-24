from .user_model import db
from datetime import datetime

class Venue(db.Model):
    __tablename__ = 'VENUES'

    events = db.relationship('Event', backref='venue', lazy=True)

class Category(db.Model):
    __tablename__ = 'CATEGORIES'
    categoryid = db.Column('CATEGORYID', db.Integer, primary_key=True)
    categoryname = db.Column('CATEGORYNAME', db.String(100))
    events = db.relationship('Event', backref='category', lazy=True)

class Event(db.Model):
    __tablename__ = 'EVENTS'


    registrations = db.relationship('Registration', backref='event', lazy=True)
    payments = db.relationship('Payment', backref='event', lazy=True)
    feedbacks = db.relationship('Feedback', backref='event', lazy=True)
    schedules = db.relationship('EventSchedule', backref='event', lazy=True)

class EventSchedule(db.Model):
    __tablename__ = 'EVENT_SCHEDULE'

