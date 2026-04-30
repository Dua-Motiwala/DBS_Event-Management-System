from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.user_model import db
from sqlalchemy import text
from models.event_model import Event
from models.registration_model import Registration, Payment, Feedback
import oracledb

attendee_bp = Blueprint('attendee', __name__)

@attendee_bp.route('/dashboard')
@login_required
def dashboard():
    registrations = Registration.query.filter_by(userid=current_user.userid).all()
    return render_template('dashboards/attendee.html', registrations=registrations)

def register_and_pay(event_id):
    try:
        import oracledb
        
        # Register User
        cursor = db.session.connection().connection.cursor()
        v_status = cursor.var(oracledb.STRING)

        cursor.execute(
            "BEGIN sp_Register_For_Event(:uid, :eid, :status); END;",
            uid=current_user.userid,
            eid=event_id,
            status=v_status
        )

        status = v_status.getvalue()

        if status != 'SUCCESS':
            if status == 'ALREADY_REGISTERED':
                flash('Already registered for this event.', 'info')
            else:
                flash(f'Registration failed: {status}', 'danger')
            return redirect(url_for('attendee.dashboard'))

        # Check Payment 
        existing = Payment.query.filter_by(
            userid=current_user.userid,
            eventid=event_id
        ).first()

        if existing:
            flash('Already registered and paid for this event.', 'info')
            return redirect(url_for('attendee.payment_history'))

        # Create Payment
        new_payment = Payment(
            userid=current_user.userid,
            eventid=event_id,
            amount=500,
            paymentstatus='Paid'
        )

        db.session.add(new_payment)
        db.session.commit()

        flash('Registered and payment completed successfully!', 'success')
        return redirect(url_for('attendee.payment_history'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')
        return redirect(url_for('attendee.dashboard'))

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
            userid=current_user.user_id,
            eventid=event_id,
            rating=rating,
            feedbacktext=feedback_text
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        flash('Feedback Submitted', 'success')
        return redirect(url_for('attendee.dashboard'))
    
    return render_template('attendee/feedback.html', event_id=event_id)
