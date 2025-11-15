from datetime import datetime, timedelta
import pytz
from sqlalchemy import func

from flask import render_template, Blueprint, send_from_directory, jsonify, abort
from models import Faculty, Courses, Facilities, Campus, News, Notification, Galleries, Alumni, Committee

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
    alumni_list = Alumni.query.all()
    principal = {
        "photo": "images/Principal.jpeg",
        "name": "प्रो. अनिल कुमार",
        "designation": "प्राचार्य",
        "bio": " संदेश - शैक्षणिक गुणवत्ता में अभिवृद्धि करना एवं देश व समाज के लिए कुशल और योग्य नागरिक तैयार करना |"
    }
    return render_template("home.html", title="Kisan PG College", faculties=faculty_list,courses=courses_list,facilities= facilities_list, notifications=notifications
                           ,campuses=campus_list, utc_now=utc_now, today_date=today_date, two_days_ago=two_days_ago,
                           alumni_list = alumni_list,principal=principal)

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
    
    # Debug: Print all notifications
    print("=== DEBUG: Notifications ===")
    print(f"Total Notifications Found: {len(notifications)}")
    for notif in notifications:
        print(f"ID: {notif.id}, Message: {notif.message}, Photo: {notif.photo}, Created: {notif.created_at}")
    print("============================")
    
    return render_template("notifications.html", title="Notifications", notifications=notifications,
                           utc_now=utc_now, today_date=today_date, two_days_ago=two_days_ago)

@main_routes_bp.route('/sitemap.xml')
def sitemap():
    return send_from_directory(directory='.', path='sitemap.xml', mimetype='application/xml')

@main_routes_bp.route('/robots.txt')
def robots():
    return send_from_directory(directory='static', path='robots.txt', mimetype='text/plain')

@main_routes_bp.route('/gallery')
def gallery():
    gallery_items = Galleries.query.all()
    return render_template('gallery.html', title="gallery", gallery=gallery_items)

@main_routes_bp.route('/committees')
def committees():
    # Use case-insensitive filter to match types containing "college" or "management"
    committee_items = Committee.query.filter(func.lower(Committee.type).like('%college%')).all()
    management_items = Committee.query.filter(func.lower(Committee.type).like('%management%')).all()
    
    # Debug: Print all committees and their types
    all_committees = Committee.query.all()
    print("=== DEBUG: All Committees ===")
    for comm in all_committees:
        print(f"ID: {comm.id}, Name: {comm.name}, Type: '{comm.type}'")
    print(f"College Committees Found: {len(committee_items)}")
    print(f"Management Committees Found: {len(management_items)}")
    print("============================")
    
    return render_template('committees.html', title="Committees", college_committees=committee_items
                           , management_committees=management_items)

# Web route for getting a specific committee's details (for rendering in HTML)
@main_routes_bp.route('/api/committees/<int:committee_id>')
def get_committee(committee_id):
    # Fetch the committee by ID
    committee = Committee.query.get(committee_id)

    if not committee:
        abort(404, description="Committee not found")  # Returns a 404 if committee is not found

    # Serialize the committee data
    committee_data = {
        'id': committee.id,
        'name': committee.name,
        # 'description': committee.description,
        'members': []
    }

    # Add member data
    for member in committee.members:
        # Fix photo path - ensure it's properly formatted
        photo_url = f'/static/{member.photo}' if member.photo else '/static/images/default_member.jpg'
        committee_data['members'].append({
            'id': member.id,
            'name': member.name,
            'designation': member.designation,
            'bio': member.bio or 'No bio available',
            'photo': photo_url
        })

    return jsonify(committee_data)
