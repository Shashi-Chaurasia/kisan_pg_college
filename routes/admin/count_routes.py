from flask import render_template, Blueprint
from models import Facilities, Courses, Faculty, Campus, Notification, News, Galleries

count_routes_bp = Blueprint('count_routes', __name__, url_prefix='/admin')

def register_routes(app):
    app.register_blueprint(count_routes_bp);

@count_routes_bp.route("/dashboard", methods=["GET"])
def count_all_for_dashboard():
    """Route to count the number of courses in the database."""
    course_count = Courses.query.count()
    faculty_count = Faculty.query.count()
    facilities_count = Facilities.query.count()
    campus_count = Campus.query.count()
    notification_count = Notification.query.count()
    news_count = News.query.count()
    gallery_count = Galleries.query.count()
    return render_template("admin/dashboard.html",course_count=course_count, faculty_count=faculty_count,
                           facilities_count=facilities_count, campus_count=campus_count,
                           notification_count=notification_count,news_count=news_count, galleries_count=gallery_count)
