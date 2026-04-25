from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.user_model import db, User
from models.event_model import Event, Venue, Category
from models.registration_model import Payment, AdminLog
from sqlalchemy import text
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'Admin':
            flash('Access denied.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'users': User.query.count(),
        'events': Event.query.count(),
        'registrations': 0, # Add registration count later
        'payments': db.session.query(db.func.sum(Payment.amount)).scalar() or 0
    }
    return render_template('dashboards/admin.html', stats=stats)

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    try:
        # Calling Subprogram/Procedure
        db.session.execute(text("BEGIN sp_Delete_User(:uid); END;"), {"uid": user_id})
        db.session.commit()
        flash('User deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {e}', 'danger')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/events')
@login_required
@admin_required
def manage_events():
    events = Event.query.all()
    return render_template('admin/manage_events.html', events=events)

@admin_bp.route('/venues', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_venues():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        capacity = request.form.get('capacity')
        new_venue = Venue(name=name, location=location, capacity=capacity)
        db.session.add(new_venue)
        
        # Adding the action
        new_log = AdminLog(userid=current_user.userid, action=f"Added new venue: {name}")
        db.session.add(new_log)
        
        db.session.commit()
        flash('Venue added.', 'success')
    venues = Venue.query.all()
    return render_template('admin/manage_venues.html', venues=venues)

@admin_bp.route('/categories', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_categories():
    if request.method == 'POST':
        name = request.form.get('name')
        new_cat = Category(categoryname=name)
        db.session.add(new_cat)
        
        # Log the action
        new_log = AdminLog(userid=current_user.userid, action=f"Added new category: {name}")
        db.session.add(new_log)
        
        db.session.commit()
        flash('Category added.', 'success')
    categories = Category.query.all()
    return render_template('admin/manage_categories.html', categories=categories)

@admin_bp.route('/registrations')
@login_required
@admin_required
def view_registrations():
    from models.registration_model import Registration
    registrations = Registration.query.all()
    return render_template('admin/registrations.html', registrations=registrations)

@admin_bp.route('/feedback')
@login_required
@admin_required
def view_feedback():
    from models.registration_model import Feedback
    feedbacks = Feedback.query.all()
    return render_template('admin/feedback.html', feedbacks=feedbacks)

@admin_bp.route('/payments')
@login_required
@admin_required
def manage_payments():
    payments = Payment.query.all()
    return render_template('admin/manage_payments.html', payments=payments)

@admin_bp.route('/logs')
@login_required
@admin_required
def view_logs():
    logs = AdminLog.query.order_by(AdminLog.actiontime.desc()).all()
    return render_template('admin/logs.html', logs=logs)

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    # Requirement: Advanced SQL features, Joins, Built-in functions, Views
    # Using raw SQL to fetch data from the View we created
    sql = text("""
        SELECT * FROM vw_Event_Details 
        ORDER BY EventDate DESC
    """)
    event_details = db.session.execute(sql).fetchall()
    
    # Another query with built-in functions and dynamic input handling
    # Requirement: Dynamic user input handling
    category_id = request.args.get('category_id')
    if category_id:
        stats_sql = text("""
            SELECT CategoryName, COUNT(*) as EventCount 
            FROM vw_Event_Details 
            WHERE CategoryID = :cat_id 
            GROUP BY CategoryName
        """)
        stats = db.session.execute(stats_sql, {"cat_id": category_id}).fetchone()
    else:
        stats = None

    return render_template('admin/reports.html', event_details=event_details, stats=stats)
