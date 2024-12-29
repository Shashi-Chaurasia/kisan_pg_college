from flask import render_template, request, redirect, url_for, session, flash, Blueprint

from models import Courses, db

course_routes_bp = Blueprint("course_routes", __name__, url_prefix="/admin")

def register_routes(app):
    app.register_blueprint(course_routes_bp);


@course_routes_bp.route("/manage/courses")
def manage_courses():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))
    courses = Courses.query.all()
    return render_template("admin/course/manage_course.html", courses=courses)


@course_routes_bp.route("/manage/courses/edit/<int:id>", methods=["GET", "POST"])
@course_routes_bp.route("/manage/courses/add", methods=["GET", "POST"], defaults={"id": None})
def add_or_edit_courses(id):
    """Route to add or edit course details."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))
    course = Courses.query.get(id) if id else None

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description", "")

        if not title:
            flash("Title is required.", "danger")
            return render_template("admin/course/edit_course.html", course=course)

        if course:  # Update existing course
            course.title = title
            course.description = description
            flash("Course updated successfully!", "success")
        else:  # Add a new course
            course = Courses(title=title, description=description)
            db.session.add(course)
            flash("Course added successfully!", "success")

        db.session.commit()
        return redirect(url_for("course_routes.manage_courses"))

    return render_template("admin/course/edit_course.html", course=course)


@course_routes_bp.route("/manage/courses/delete/<int:id>", methods=["POST"])
def delete_courses(id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    courses = Courses.query.get_or_404(id)
    try:
        db.session.delete(courses)
        db.session.commit()
        flash("Faculty deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting faculty: {str(e)}", "error")

    return redirect(url_for("course_routes.manage_courses"))
