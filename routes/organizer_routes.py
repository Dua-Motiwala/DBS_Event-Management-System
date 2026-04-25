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
        # Extract form data
        title = request.form.get('title')
        description = request.form.get('description')
        venue_id = request.form.get('venue_id')
        category_id = request.form.get('category_id')
        
        # Basic validation
        if not title:
            flash('Event Title is required.', 'danger')
            venues = Venue.query.all()
            categories = Category.query.all()
            return render_template('organizer/create_event.html', venues=venues, categories=categories)

        # Create new event
        new_event = Event(
            userid=current_user.userid,
            title=title,
            description=description,
            venue_id=venue_id,
            category_id=category_id
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        flash('Event successfully CREATED!', 'success')
        return redirect(url_for('organizer.manage_event', event_id=new_event.event_id))

    # GET request: Render form
    venues = Venue.query.all()
    categories = Category.query.all()   
    return render_template('organizer/create_event.html', venues=venues, categories=categories)

@organizer_bp.route('/manage-event/<int:event_id>')
@login_required
@organizer_required
def manage_event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('organizer/manage_event.html', event=event)

@organizer_bp.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
@organizer_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        # Update event fields
        event.title = request.form.get('title')
        event.description = request.form.get('description')
        event.venue_id = request.form.get('venue_id')
        event.category_id = request.form.get('category_id')
        
        try:
            db.session.commit()
            flash('Event updated successfully.', 'success')
            return redirect(url_for('organizer.manage_event', event_id=event_id))
        except Exception as e:
            db.session.rollback()
            flash('Error occurred while updating the event.', 'danger')

    # GET request: Render form with current data
    venues = Venue.query.all()
    categories = Category.query.all()
    return render_template('organizer/edit_event.html', event=event, venues=venues, categories=categories)

@organizer_bp.route('/event-schedule/<int:event_id>', methods=['GET', 'POST'])
@login_required
@organizer_required
def manage_schedule(event_id):
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        # Handle adding a schedule slot
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        activity_name = request.form.get('activity_name')
        
        if start_time and end_time and activity_name:
            new_schedule = EventSchedule(
                event_id=event_id,
                start_time=start_time,
                end_time=end_time,
                activity_name=activity_name
            )
            db.session.add(new_schedule)
            db.session.commit()
            flash('Schedule item added.', 'success')
        else:
            flash('Please fill in all schedule fields.', 'danger')

    # GET request: Render schedule form
    venues = Venue.query.all()
    categories = Category.query.all()
    return render_template('organizer/schedule.html', event=event)

@organizer_bp.route('/participants/<int:event_id>')
@login_required
@organizer_required
def view_participants(event_id):
    event = Event.query.get_or_404(event_id)
    participants = Registration.query.filter_by(event_id=event_id).all()
    feedbacks = Feedback.query.filter_by(event_id=event_id).all()
    return render_template('organizer/participants.html', event=event, participants=participants, feedbacks=feedbacks)

@organizer_bp.route('/feedback/<int:event_id>')
@login_required
@organizer_required
def view_feedback(event_id):
    event = Event.query.get_or_404(event_id)
    feedbacks = Feedback.query.filter_by(event_id=event_id).all()
    return render_template('organizer/feedback.html', event=event, feedbacks=feedbacks)

@organizer_bp.route('/delete-event/<int:event_id>', methods=['POST'])
@login_required
@organizer_required
def delete_event(event_id):    
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully.', 'success')
    return redirect(url_for('organizer.dashboard'))
