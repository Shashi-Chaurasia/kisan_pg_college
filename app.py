from flask import Flask
from flask_wtf.csrf import CSRFProtect
from models import db
from routes import main_routes
from routes.admin import admin_routes, faculty_routes, course_routes, facilities_routes, count_routes, campus_routes, \
    notification_routes, news_routes, gallery_routes, alumni_routes, committees_routes
from flask_migrate import Migrate
from config import config
import os

csrf = CSRFProtect()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    Migrate(app, db)
    # Register blueprints
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

    # Initialize the database if running for the first time
    with app.app_context():
        db.create_all()

    return app

# Expose WSGI callable as "application"
application = create_app()

if __name__ == "__main__":
    application.run(port=5005, debug=True)