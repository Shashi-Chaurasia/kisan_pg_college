import os
from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from models import db, Alumni
from werkzeug.utils import secure_filename

alumni_routes_bp = Blueprint("alumni_routes", __name__, url_prefix="/admin")

def register_routes(app):
    app.register_blueprint(alumni_routes_bp);

UPLOAD_FOLDER = "static/uploads/alumni"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@alumni_routes_bp.route("/manage/alumni", methods=["GET", "POST"])
def manage_alumni():
    """Route to manage alumni - List and Add new alumni."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))
    alumni = Alumni.query.all()
    return render_template("admin/alumni/manage_alumni.html", alumni=alumni)

@alumni_routes_bp.route("/manage/alumni/edit/<int:id>", methods=["GET", "POST"])
@alumni_routes_bp.route("/manage/alumni/add", methods=["GET", "POST"], defaults={"id": None})
def add_or_edit_alumni(id):
    """Route to add or edit alumni details."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    alumni = Alumni.query.get(id) if id else None
    if request.method == "POST":
        name = request.form["name"]
        designation = request.form["designation"]
        bio = request.form.get("bio", "")
        year = request.form["year"]
        photo = request.files.get("photo")
        if alumni:
            alumni.name = name
            alumni.designation = designation
            alumni.bio = bio
            alumni.year = year
            if photo:
                filename = secure_filename(photo.filename)
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
                alumni.photo = os.path.join("uploads/alumni", filename)
        else:
            filename = secure_filename(photo.filename) if photo else None
            relative_photo_path = (
                os.path.join("uploads/alumni", filename) if filename else None
            )
            if photo:
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
            alumni = Alumni(name=name, designation=designation, bio=bio, year=year, photo=relative_photo_path)
            db.session.add(alumni)

        db.session.commit()
        flash(f"alumni {'updated' if id else 'added'} successfully!", "success")
        return redirect(url_for("alumni_routes.manage_alumni"))

    return render_template("admin/alumni/edit_alumni.html", alumni=alumni)

@alumni_routes_bp.route("/manage/alumni/delete/<int:id>", methods=["POST"])
def delete_alumni(id):
    """Route to delete alumni."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    alumni = Alumni.query.get_or_404(id)
    try:
        db.session.delete(alumni)
        db.session.commit()
        flash("alumni deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting alumni: {str(e)}", "error")

    return redirect(url_for("alumni_routes.manage_alumni"))
