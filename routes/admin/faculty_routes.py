import os
from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from models import db, Faculty
from werkzeug.utils import secure_filename

faculty_routes_bp = Blueprint("faculty_routes", __name__, url_prefix="/admin")

def register_routes(app):
    app.register_blueprint(faculty_routes_bp);

UPLOAD_FOLDER = "static/uploads/faculty"
PDF_FOLDER = "static/uploads/faculty/pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

@faculty_routes_bp.route("/manage/faculty", methods=["GET", "POST"])
def manage_faculty():
    """Route to manage faculty - List and Add new faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))
    faculties = Faculty.query.all()
    return render_template("admin/faculty/manage_faculty.html", faculties=faculties)

@faculty_routes_bp.route("/manage/faculty/edit/<int:id>", methods=["GET", "POST"])
@faculty_routes_bp.route("/manage/faculty/add", methods=["GET", "POST"], defaults={"id": None})
def add_or_edit_faculty(id):
    """Route to add or edit faculty details."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    faculty = Faculty.query.get(id) if id else None
    if request.method == "POST":
        name = request.form["name"]
        designation = request.form["designation"]
        bio = request.form.get("bio", "")
        photo = request.files.get("photo")
        achievement_pdf = request.files.get("achievement_pdf")
        
        if faculty:
            faculty.name = name
            faculty.designation = designation
            faculty.bio = bio
            if photo:
                filename = secure_filename(photo.filename)
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_path)
                faculty.photo = os.path.join("uploads/faculty", filename)
            if achievement_pdf and achievement_pdf.filename:
                filename = secure_filename(achievement_pdf.filename)
                if filename.lower().endswith('.pdf'):
                    pdf_path = os.path.join(PDF_FOLDER, filename)
                    achievement_pdf.save(pdf_path)
                    faculty.achievement_pdf = os.path.join("uploads/faculty/pdfs", filename)
        else:
            photo_filename = secure_filename(photo.filename) if photo else None
            relative_photo_path = (
                os.path.join("uploads/faculty", photo_filename) if photo_filename else None
            )
            achievement_pdf_path = None
            
            if photo:
                photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
                photo.save(photo_path)
            if achievement_pdf and achievement_pdf.filename:
                filename = secure_filename(achievement_pdf.filename)
                if filename.lower().endswith('.pdf'):
                    pdf_path = os.path.join(PDF_FOLDER, filename)
                    achievement_pdf.save(pdf_path)
                    achievement_pdf_path = os.path.join("uploads/faculty/pdfs", filename)
            
            faculty = Faculty(
                name=name, 
                designation=designation, 
                bio=bio, 
                photo=relative_photo_path,
                achievement_pdf=achievement_pdf_path
            )
            db.session.add(faculty)

        db.session.commit()
        flash(f"Faculty {'updated' if id else 'added'} successfully!", "success")
        return redirect(url_for("faculty_routes.manage_faculty"))

    return render_template("admin/faculty/edit_faculty.html", faculty=faculty)

@faculty_routes_bp.route("/manage/faculty/delete/<int:id>", methods=["POST"])
def delete_faculty(id):
    """Route to delete faculty."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    faculty = Faculty.query.get_or_404(id)
    try:
        # Delete associated files
        if faculty.photo:
            photo_path = os.path.join("static", faculty.photo)
            if os.path.exists(photo_path):
                try:
                    os.remove(photo_path)
                except OSError:
                    pass
        
        if faculty.achievement_pdf:
            pdf_path = os.path.join("static", faculty.achievement_pdf)
            if os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                except OSError:
                    pass
        
        # Delete the faculty record
        db.session.delete(faculty)
        db.session.commit()
        flash("Faculty deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting faculty: {str(e)}", "error")

    return redirect(url_for("faculty_routes.manage_faculty"))
