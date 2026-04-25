from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.user_model import db
from sqlalchemy import text
from models.event_model import Event
from models.registration_model import Registration, Payment, Feedback

attendee_bp = Blueprint('attendee', __name__)

@attendee_bp.route('/dashboard')
@login_required
def dashboard():
    registrations = Registration.query.filter_by(userid=current_user.userid).all()
    return render_template('dashboards/attendee.html', registrations=registrations)

@attendee_bp.route('/register-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def register_event(event_id):
    
    #
        
    return redirect(url_for('attendee.dashboard'))

@attendee_bp.route('/make-payment/<int:event_id>', methods=['GET', 'POST'])
@login_required
def make_payment(event_id):
    
    # 
    
    return render_template('attendee/make_payment.html', event_id=event_id)

@attendee_bp.route('/my-registrations')
@login_required
def my_registrations():
    
    #
    
    return render_template('attendee/my_registrations.html', registrations=registrations)

@attendee_bp.route('/payments')
@login_required
def payment_history():
    
    #
    
    return render_template('attendee/payments.html', payments=payments)

@attendee_bp.route('/feedback/<int:event_id>', methods=['GET', 'POST'])
@login_required
def give_feedback(event_id):
    
    # 
    
    return render_template('attendee/feedback.html', event_id=event_id)
