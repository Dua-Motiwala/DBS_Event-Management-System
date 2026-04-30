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
    if request.method == 'POST':
        title = request.form.get('title')
        date_str = request.form.get('date')
        venue_id = request.form.get('venue')
        category_id = request.form.get('category')
        
        from datetime import datetime
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        new_event = Event(
            title=title, 
            eventdate=event_date, 
            venueid=venue_id, 
            categoryid=category_id, 
            userid=current_user.userid
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('organizer.dashboard'))
        
    venues = Venue.query.all()
    categories = Category.query.all()
    return render_template('organizer/create_event.html', venues=venues, categories=categories)

@organizer_bp.route('/manage-event/<int:event_id>')
@login_required
@organizer_required
def manage_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.userid != current_user.userid:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('organizer.dashboard'))
    return render_template('organizer/manage_event.html', event=event)

@organizer_bp.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
@organizer_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.userid != current_user.userid:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('organizer.dashboard'))
        
    if request.method == 'POST':
        event.title = request.form.get('title')
        date_str = request.form.get('date')
        from datetime import datetime
        event.eventdate = datetime.strptime(date_str, '%Y-%m-%d').date()
        event.venueid = request.form.get('venue')
        event.categoryid = request.form.get('category')
        
        db.session.commit()
        flash('Event updated!', 'success')
        return redirect(url_for('organizer.manage_event', event_id=event_id))
        
    venues = Venue.query.all()
    categories = Category.query.all()
    return render_template('organizer/edit_event.html', event=event, venues=venues, categories=categories)

@organizer_bp.route('/event-schedule/<int:event_id>', methods=['GET', 'POST'])
@login_required
@organizer_required
def manage_schedule(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        start_str = request.form.get('start_time')
        end_str = request.form.get('end_time')
        
        try:
            from datetime import datetime
            # Format from HTML datetime-local is YYYY-MM-DDTHH:MM
            start_time = datetime.strptime(start_str, '%Y-%m-%dT%H:%M')
            end_time = datetime.strptime(end_str, '%Y-%m-%dT%H:%M')
            
            new_slot = EventSchedule(eventid=event_id, starttime=start_time, endtime=end_time)
            db.session.add(new_slot)
            db.session.commit()
            flash('Schedule slot added!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding schedule: {e}', 'danger')
            
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
    
@organizer_bp.route('/cancel-registration/<int:reg_id>', methods=['POST'])
@login_required
@organizer_required
def cancel_registration(reg_id):
    registration = Registration.query.get_or_404(reg_id)
    # Security: Ensure this event belongs to the organizer
    if registration.event.userid != current_user.userid:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('organizer.dashboard'))
    
    try:
        db.session.delete(registration)
        db.session.commit()
        flash('Registration has been cancelled.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')
        
    return redirect(url_for('organizer.view_participants', event_id=registration.eventid))

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
