from flask import Flask
from models import db
from routes import main_routes
from routes.admin import admin_routes, faculty_routes, course_routes, facilities_routes, count_routes, campus_routes, \
    notification_routes, news_routes, gallery_routes
from flask_migrate import Migrate

from routes.admin.gallery_routes import gallery_routes_bp


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kishanpgcollege.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key'
    UPLOAD_FOLDER = 'static/uploads/faculty'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
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

    # Initialize the database if running for the first time
    with app.app_context():
        db.create_all()

    return app

# Expose WSGI callable as "application"
application = create_app()

if __name__ == "__main__":
    application.run(port=5005, debug=True)