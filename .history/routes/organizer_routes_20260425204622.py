from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.user_model import db
from sqlalchemy import text
from models.event_model import Event, Venue, Category, EventSchedule
from models.registration_model import Registration, Feedback

organizer_bp = Blueprint('organizer', __name__)

def organizer_required(f):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'Organizer':
            flash('Access denied.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@organizer_bp.route('/dashboard')
@login_required
@organizer_required
def dashboard():
    my_events = Event.query.filter_by(userid=current_user.userid).all()
    return render_template('dashboards/organizer.html', events=my_events)

@organizer_bp.route('/create-event', methods=['GET', 'POST'])
@login_required
@organizer_required
def create_event():
    
    # Organizer creates a new event
    
    return render_template('organizer/create_event.html', venues=venues, categories=categories)

@organizer_bp.route('/manage-event/<int:event_id>')
@login_required
@organizer_required
def manage_event(event_id):
    
    # View single event details
    
    return render_template('organizer/manage_event.html', event=event)

@organizer_bp.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
@organizer_required
def edit_event(event_id):

    # Update event information
    
    return render_template('organizer/edit_event.html', event=event, venues=venues, categories=categories)

@organizer_bp.route('/event-schedule/<int:event_id>', methods=['GET', 'POST'])
@login_required
@organizer_required
def manage_schedule(event_id):

    $
    return render_template('organizer/schedule.html', event=event)

@organizer_bp.route('/participants/<int:event_id>')
@login_required
@organizer_required
def view_participants(event_id):
    event = Event.query.get_or_404(event_id)
    participants = Registration.query.filter_by(eventid=event_id).all()
    return render_template('organizer/participants.html', event=event, participants=participants)

@organizer_bp.route('/feedback/<int:event_id>')
@login_required
@organizer_required
def view_feedback(event_id):
    event = Event.query.get_or_404(event_id)
    feedbacks = Feedback.query.filter_by(eventid=event_id).all()
    return render_template('organizer/feedback.html', event=event, feedbacks=feedbacks)

@organizer_bp.route('/delete-event/<int:event_id>', methods=['POST'])
@login_required
@organizer_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.userid != current_user.userid:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('organizer.dashboard'))
    
    try:
        # Calling Subprogram (Requirement: Program/Subprogram)
        db.session.execute(text("BEGIN sp_Cancel_Event(:eid); END;"), {"eid": event_id})
        db.session.commit()
        flash('Event cancelled and deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error cancelling event: {e}', 'danger')
    
    return redirect(url_for('organizer.dashboard'))
