from .user_model import db
from datetime import datetime

class Registration(db.Model):
    __tablename__ = 'REGISTRATIONS'


class Payment(db.Model):
    __tablename__ = 'PAYMENTS'


class Feedback(db.Model):
    __tablename__ = 'FEEDBACK'


class AdminLog(db.Model):
    __tablename__ = 'ADMIN_LOG'

