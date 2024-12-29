import os
from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from models import db ,News
from werkzeug.utils import secure_filename

news_routes_bp = Blueprint("news_routes", __name__, url_prefix="/admin")

def register_routes(app):
    app.register_blueprint(news_routes_bp);

UPLOAD_FOLDER = "static/uploads/news"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@news_routes_bp.route("/manage/news", methods=["GET", "POST"])
def manage_news():
    """Route to manage faculty - List and Add new faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))
    news = News.query.all()
    return render_template("admin/news/manage_news.html", news=news)

@news_routes_bp.route("/manage/news/edit/<int:id>", methods=["GET", "POST"])
@news_routes_bp.route("/manage/news/add", methods=["GET", "POST"], defaults={"id": None})
def add_or_edit_news(id):
    """Route to add or edit faculty details."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    news = News.query.get(id) if id else None
    if request.method == "POST":
        title = request.form["title"]
        content = request.form.get("content", "")
        photo = request.files.get("photo")
        if news:
            news.title = title
            news.content = content
            if photo:
                filename = secure_filename(photo.filename)
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
                news.photo = os.path.join("uploads/news", filename)
        else:
            filename = secure_filename(photo.filename) if photo else None
            relative_photo_path = (
                os.path.join("uploads/news", filename) if filename else None
            )
            if photo:
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
            news = News(title=title,  content=content, photo=relative_photo_path)
            db.session.add(news)

        db.session.commit()
        flash(f"Faculty {'updated' if id else 'added'} successfully!", "success")
        return redirect(url_for("news_routes.manage_news"))

    return render_template("admin/news/edit_news.html", news=news)

@news_routes_bp.route("/manage/news/delete/<int:id>", methods=["POST"])
def delete_news(id):
    """Route to delete faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    news = News.query.get_or_404(id)
    try:
        db.session.delete(news)
        db.session.commit()
        flash("Faculty deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting faculty: {str(e)}", "error")

    return redirect(url_for("news_routes.manage_news"))
