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
    try:
        # Calling Subprogram with OUT parameter (Requirement: Program/Subprogram)
        # In Oracle, we can use a PL/SQL block to get the OUT parameter
        import oracledb
        cursor = db.session.connection().connection.cursor()
        v_status = cursor.var(oracledb.STRING)
        cursor.execute("BEGIN sp_Register_For_Event(:uid, :eid, :status); END;", 
                       uid=current_user.userid, eid=event_id, status=v_status)
        
        status = v_status.getvalue()
        
        if status == 'SUCCESS':
            db.session.commit()
            flash('Successfully registered for the event!', 'success')
        elif status == 'ALREADY_REGISTERED':
            flash('You are already registered for this event.', 'info')
        else:
            flash(f'Registration failed: {status}', 'danger')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error during registration: {e}', 'danger')
        
    return redirect(url_for('attendee.dashboard'))

@attendee_bp.route('/make-payment/<int:event_id>', methods=['GET', 'POST'])
@login_required
def make_payment(event_id):
    if request.method == 'POST':
        amount = request.form.get('amount')
        new_payment = Payment(userid=current_user.userid, eventid=event_id, amount=amount, paymentstatus='Paid')
        db.session.add(new_payment)
        db.session.commit()
        flash('Payment recorded successfully!', 'success')
        return redirect(url_for('attendee.payment_history'))
    return render_template('attendee/make_payment.html', event_id=event_id)

@attendee_bp.route('/my-registrations')
@login_required
def my_registrations():
    registrations = Registration.query.filter_by(userid=current_user.userid).all()
    return render_template('attendee/my_registrations.html', registrations=registrations)

@attendee_bp.route('/payments')
@login_required
def payment_history():
    payments = Payment.query.filter_by(userid=current_user.userid).all()
    return render_template('attendee/payments.html', payments=payments)

@attendee_bp.route('/feedback/<int:event_id>', methods=['GET', 'POST'])
@login_required
def give_feedback(event_id):
    
    # 
    return render_template('attendee/feedback.html', event_id=event_id)
