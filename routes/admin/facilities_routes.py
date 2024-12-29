import os
from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from models import db,Facilities
from werkzeug.utils import secure_filename

facilities_routes_bp = Blueprint("facilities_routes", __name__, url_prefix="/admin")

def register_routes(app):
    app.register_blueprint(facilities_routes_bp);

UPLOAD_FOLDER = "static/uploads/facilities"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@facilities_routes_bp.route("/manage/facilities", methods=["GET", "POST"])
def manage_facilities():
    """Route to manage faculty - List and Add new faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))
    facilities = Facilities.query.all()
    return render_template("admin/facilities/manage_facilities.html", facilities=facilities)

@facilities_routes_bp.route("/manage/facilities/edit/<int:id>", methods=["GET", "POST"])
@facilities_routes_bp.route("/manage/facilities/add", methods=["GET", "POST"], defaults={"id": None})
def add_or_edit_facilities(id):
    """Route to add or edit faculty details."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    facilities = Facilities.query.get(id) if id else None
    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description", "")
        photo = request.files.get("photo")
        if facilities:
            facilities.title = title
            facilities.description = description
            if photo:
                filename = secure_filename(photo.filename)
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
                facilities.photo = os.path.join("uploads/facilities", filename)
        else:
            filename = secure_filename(photo.filename) if photo else None
            relative_photo_path = (
                os.path.join("uploads/facilities", filename) if filename else None
            )
            if photo:
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
            facilities = Facilities(title=title,  description=description, photo=relative_photo_path)
            db.session.add(facilities)

        db.session.commit()
        flash(f"Faculty {'updated' if id else 'added'} successfully!", "success")
        return redirect(url_for("facilities_routes.manage_facilities"))

    return render_template("admin/facilities/edit_facilities.html", facilities=facilities)

@facilities_routes_bp.route("/manage/facilities/delete/<int:id>", methods=["POST"])
def delete_facilities(id):
    """Route to delete faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    facilities = Facilities.query.get_or_404(id)
    try:
        db.session.delete(facilities)
        db.session.commit()
        flash("Faculty deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting faculty: {str(e)}", "error")

    return redirect(url_for("facilities_routes.manage_facilities"))
