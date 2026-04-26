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

    # Registers user for an event using a stored procedure
    if request.method == 'POST':
        registration = Registration(
            regid=regid,#should this be surrogate key(auto incrementing)
            userid=current_user.user_id,
            eventid=event_id
        )
        
        db.session.add(registration)
        db.session.commit()
        
        flash('Registered for Event Successfully', 'success')
    return redirect(url_for('attendee.dashboard'))      

@attendee_bp.route('/make-payment/<int:event_id>', methods=['GET', 'POST'])
@login_required
def make_payment(event_id):
    
    # Stores payment details for an event
    if request.method == 'POST':
        amount = request.form.get('amount')
        paymentstatus = request.form.get('paymentstatus')

        payment = Payment(
            paymentid=paymentid,#should this be surrogate key(auto incrementing)
            userid=current_user.user_id,
            eventid=event_id,
            paymentstatus=paymentstatus
            amount=amount
        )
        
        db.session.add(payment)
        db.session.commit()
        
        flash('Transaction Completed Successfully', 'success')
        return redirect(url_for('attendee.dashboard'))
    
    return render_template('attendee/make_payment.html', event_id=event_id)

@attendee_bp.route('/my-registrations')
@login_required
def my_registrations():
    
    # Shows all events the user has registered for
    registrations=Registration.query.filter_by(userid=current_user.userid).all()
    return render_template('attendee/my_registrations.html', registrations=registrations)

@attendee_bp.route('/payments')
@login_required
def payment_history():
    
    # Shows all payments made by the user
    payments=Payment.query.filter_by(userid=current_user.userid).all()
    return render_template('attendee/payments.html', payments=payments)

@attendee_bp.route('/feedback/<int:event_id>', methods=['GET', 'POST'])
@login_required
def give_feedback(event_id):
    
    # Lets user submit rating and comments for an event
    if request.method == 'POST':
        rating = request.form.get('rating')
        feedback_text = request.form.get('feedback_text')

        feedback = Feedback(
            feedbackid=feedback_id,#should this be surrogate key(auto incrementing)
            userid=current_user.user_id,
            eventid=event_id,
            rating=rating
            feedbacktext=feedback_text
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        flash('Feedback Submitted', 'success')
        return redirect(url_for('attendee.dashboard'))
    
    return render_template('attendee/feedback.html', event_id=event_id)
