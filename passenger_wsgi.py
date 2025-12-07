import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Change to the application directory (important for cPanel)
os.chdir(os.path.dirname(__file__))

# Import the Flask application
try:
    from app import application
except ImportError as e:
    # If import fails, try creating the app directly
    try:
        from app import create_app
        application = create_app()
    except Exception as e2:
        # Last resort: create app inline
        from flask import Flask
        from flask_wtf.csrf import CSRFProtect
        from models import db
        from routes import main_routes
        from routes.admin import admin_routes, faculty_routes, course_routes, facilities_routes, count_routes, campus_routes, \
            notification_routes, news_routes, gallery_routes, alumni_routes, committees_routes
        from flask_migrate import Migrate
        from config import config
        
        csrf = CSRFProtect()
        
        app = Flask(__name__)
        config_name = os.environ.get('FLASK_ENV', 'production')
        app.config.from_object(config.get(config_name, config['default']))
        
        db.init_app(app)
        csrf.init_app(app)
        Migrate(app, db)
        
        main_routes.register_routes(app)
        admin_routes.register_routes(app)
        faculty_routes.register_routes(app)
        course_routes.register_routes(app)
        facilities_routes.register_routes(app)
        count_routes.register_routes(app)
        campus_routes.register_routes(app)
        notification_routes.register_routes(app)
        news_routes.register_routes(app)
        gallery_routes.register_routes(app)
        alumni_routes.register_routes(app)
        committees_routes.register_routes(app)
        
        with app.app_context():
            db.create_all()
        
        application = app
