from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager
from models.user_model import db, User
from config import Config
import oracledb

# Initialize extensions
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize oracledb in thick mode if needed for older DB versions
    try:
        oracledb.init_oracle_client()
    except Exception as e:
        print(f"Oracle Client initialization failed: {e}")
        # If it fails, it might already be initialized or Instant Client is missing.
        # Thin mode (default) will be used if init_oracle_client() is not called.
        pass

    # Initialize DB
    db.init_app(app)
    
    # Initialize Login Manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.admin_routes import admin_bp
    from routes.organizer_routes import organizer_bp
    from routes.attendee_routes import attendee_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(organizer_bp, url_prefix='/organizer')
    app.register_blueprint(attendee_bp, url_prefix='/attendee')

    @app.route('/event/<int:event_id>')
    def event_details(event_id):
        from models.event_model import Event
        event = Event.query.get_or_404(event_id)
        return render_template('event_details.html', event=event)

    @app.route('/')
    def index():
        from models.event_model import Event
        search_query = request.args.get('search')
        if search_query:
            # Simple search by title
            events = Event.query.filter(Event.title.ilike(f'%{search_query}%')).all()
        else:
            events = Event.query.order_by(Event.eventdate.desc()).limit(6).all()
        return render_template('index.html', events=events)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        # Note: In production, use migrations.
        # db.create_all() 
        pass
    app.run(debug=True)
