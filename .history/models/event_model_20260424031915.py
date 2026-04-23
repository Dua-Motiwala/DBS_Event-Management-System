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
h

class EventSchedule(db.Model):
    __tablename__ = 'EVENT_SCHEDULE'
    