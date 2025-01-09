import os
from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from models import db ,Galleries
from werkzeug.utils import secure_filename

gallery_routes_bp = Blueprint("gallery_routes", __name__, url_prefix="/admin")

def register_routes(app):
    app.register_blueprint(gallery_routes_bp);

UPLOAD_FOLDER = "static/uploads/gallery"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@gallery_routes_bp.route("/manage/gallery", methods=["GET", "POST"])
def manage_gallery():
    """Route to manage faculty - List and Add new faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))
    gallery = Galleries.query.all()
    return render_template("admin/gallery/manage_gallery.html", gallery=gallery)

@gallery_routes_bp.route("/manage/gallery/edit/<int:id>", methods=["GET", "POST"])
@gallery_routes_bp.route("/manage/gallery/add", methods=["GET", "POST"], defaults={"id": None})
def add_or_edit_gallery(id):
    """Route to add or edit faculty details."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    gallery = Galleries.query.get(id) if id else None
    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description", "")
        photo = request.files.get("photo")
        if gallery:
            gallery.title = title
            gallery.description = description
            if photo:
                filename = secure_filename(photo.filename)
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
                gallery.photo = os.path.join("uploads/gallery", filename)
        else:
            filename = secure_filename(photo.filename) if photo else None
            relative_photo_path = (
                os.path.join("uploads/gallery", filename) if filename else None
            )
            if photo:
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
            gallery = Galleries(title=title,  description=description, photo=relative_photo_path)
            db.session.add(gallery)

        db.session.commit()
        flash(f"Gallery {'updated' if id else 'added'} successfully!", "success")
        return redirect(url_for("gallery_routes.manage_gallery"))

    return render_template("admin/gallery/edit_gallery.html", gallery=gallery)

@gallery_routes_bp.route("/manage/gallery/delete/<int:id>", methods=["POST"])
def delete_gallery(id):
    """Route to delete faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    gallery = Galleries.query.get_or_404(id)
    try:
        db.session.delete(gallery)
        db.session.commit()
        flash("Faculty deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting faculty: {str(e)}", "error")

    return redirect(url_for("gallery_routes.manage_gallery"))
