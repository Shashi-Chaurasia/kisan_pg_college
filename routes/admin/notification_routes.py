import os
from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from models import db,Notification
from werkzeug.utils import secure_filename

notification_routes_bp = Blueprint("notification_routes", __name__, url_prefix="/admin")

def register_routes(app):
    app.register_blueprint(notification_routes_bp)

UPLOAD_FOLDER = "static/uploads/notification"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@notification_routes_bp.route("/manage/notification", methods=["GET", "POST"])
def manage_notification():
    """Route to manage faculty - List and Add new faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))
    notification = Notification.query.all()
    return render_template("admin/notification/manage_notification.html", notification=notification)

@notification_routes_bp.route("/manage/notification/edit/<int:id>", methods=["GET", "POST"])
@notification_routes_bp.route("/manage/notification/add", methods=["GET", "POST"], defaults={"id": None})
def add_or_edit_notification(id):
    """Route to add or edit faculty details."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    notification = Notification.query.get(id) if id else None
    if request.method == "POST":
        message = request.form["message"]
        photo = request.files.get("file")
        if notification:
            notification.message = message
            if photo:
                filename = secure_filename(photo.filename)
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
                notification.photo = os.path.join("uploads/notification", filename)
        else:
            filename = secure_filename(photo.filename) if photo else None
            relative_photo_path = (
                os.path.join("uploads/notification", filename) if filename else None
            )
            if photo:
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
            notification = Notification(message=message, photo=relative_photo_path)
            db.session.add(notification)

        db.session.commit()
        flash(f"Faculty {'updated' if id else 'added'} successfully!", "success")
        return redirect(url_for("notification_routes.manage_notification"))

    return render_template("admin/notification/edit_notification.html", notification=notification)

@notification_routes_bp.route("/manage/notification/delete/<int:id>", methods=["POST"])
def delete_notification(id):
    """Route to delete faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    notification = Notification.query.get_or_404(id)
    try:
        db.session.delete(notification)
        db.session.commit()
        flash("Faculty deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting faculty: {str(e)}", "error")

    return redirect(url_for("notification_routes.manage_notification"))
