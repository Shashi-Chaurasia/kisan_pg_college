from datetime import datetime, timedelta
import pytz

from flask import render_template, Blueprint, send_from_directory
from models import Faculty, Courses, Facilities, Campus, News, Notification

main_routes_bp = Blueprint('main_routes', __name__)

def register_routes(app):
    app.register_blueprint(main_routes_bp)


@main_routes_bp.route("/")
def home():
    utc_now = datetime.now(pytz.UTC)
    today_date = utc_now.strftime('%Y-%m-%d')
    two_days_ago = (utc_now - timedelta(days=2)).strftime('%Y-%m-%d')
    faculty_list = Faculty.query.all()
    courses_list = Courses.query.all()
    facilities_list = Facilities.query.all()
    campus_list = Campus.query.all()
    notifications = Notification.query.all()
    return render_template("home.html", title="Kisan PG College", faculties=faculty_list,courses=courses_list,facilities= facilities_list, notifications=notifications
                           ,campuses=campus_list, utc_now=utc_now, today_date=today_date, two_days_ago=two_days_ago)

@main_routes_bp.route("/news")
def news():
    all_news = News.query.all()
    return render_template("news.html", title="News", news=all_news)

@main_routes_bp.route('/news/<int:news_id>')
def news_detail(news_id):
    news_item = News.query.get_or_404(news_id)  # Fetch the news item by ID
    return render_template('news_detail.html', news_item=news_item)

@main_routes_bp.route("/about")
def about_us():
    return render_template("about.html")

@main_routes_bp.route("/contact")
def contact():
    return render_template("contact.html")

@main_routes_bp.route("/courses")
def courses():
    return render_template("course.html")

@main_routes_bp.route("/admission")
def academics_admission():
    return render_template("admission.html")

@main_routes_bp.route("/fees")
def academics_fees():
    return render_template("fee.html")


@main_routes_bp.route("/notification")
def notification():
    utc_now = datetime.now(pytz.UTC)
    today_date = utc_now.strftime('%Y-%m-%d')
    two_days_ago = (utc_now - timedelta(days=2)).strftime('%Y-%m-%d')
    notifications = Notification.query.all()
    return render_template("notifications.html", title="Notifications", notifications=notifications,
                           utc_now=utc_now, today_date=today_date, two_days_ago=two_days_ago)

@main_routes_bp.route('/sitemap.xml')
def sitemap():
    return send_from_directory(directory='.', path='sitemap.xml', mimetype='application/xml')