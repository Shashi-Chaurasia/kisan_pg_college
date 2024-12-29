import os
from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from models import db,Campus
from werkzeug.utils import secure_filename

campus_routes_bp = Blueprint("campus_routes", __name__, url_prefix="/admin")

def register_routes(app):
    app.register_blueprint(campus_routes_bp)

UPLOAD_FOLDER = "static/uploads/campus"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@campus_routes_bp.route("/manage/campus", methods=["GET", "POST"])
def manage_campus():
    """Route to manage faculty - List and Add new faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))
    campus = Campus.query.all()
    return render_template("admin/campus/manage_campus.html", campus=campus)

@campus_routes_bp.route("/manage/campus/edit/<int:id>", methods=["GET", "POST"])
@campus_routes_bp.route("/manage/campus/add", methods=["GET", "POST"], defaults={"id": None})
def add_or_edit_campus(id):
    """Route to add or edit faculty details."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    campus = Campus.query.get(id) if id else None
    if request.method == "POST":
        title = request.form["title"]
        photo = request.files.get("photo")
        if campus:
            campus.title = title
            if photo:
                filename = secure_filename(photo.filename)
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
                campus.photo = os.path.join("uploads/campus", filename)
        else:
            filename = secure_filename(photo.filename) if photo else None
            relative_photo_path = (
                os.path.join("uploads/campus", filename) if filename else None
            )
            if photo:
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
            campus = Campus(title=title, photo=relative_photo_path)
            db.session.add(campus)

        db.session.commit()
        flash(f"Faculty {'updated' if id else 'added'} successfully!", "success")
        return redirect(url_for("campus_routes.manage_campus"))

    return render_template("admin/campus/edit_campus.html", campus=campus)

@campus_routes_bp.route("/manage/campus/delete/<int:id>", methods=["POST"])
def delete_campus(id):
    """Route to delete faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    campus = Campus.query.get_or_404(id)
    try:
        db.session.delete(campus)
        db.session.commit()
        flash("Faculty deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting faculty: {str(e)}", "error")

    return redirect(url_for("campus_routes.manage_campus"))
