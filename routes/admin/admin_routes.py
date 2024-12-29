from flask import render_template, request, redirect, url_for, session, flash, current_app, Blueprint
from models import Admin, Faculty
from werkzeug.security import check_password_hash

admin_routes_bp = Blueprint('admin_routes', __name__, url_prefix='/admin')

def register_routes(app):
    app.register_blueprint(admin_routes_bp)

@admin_routes_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session["admin_logged_in"] = True
            return redirect(url_for("count_routes.count_all_for_dashboard"))
        flash("Invalid username or password", "danger")
    return render_template("admin/admin_login.html", title="Admin Login")


@admin_routes_bp.route("/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_routes.admin_login"))

# @admin_routes_bp.route("/dashboard")
# def admin_dashboard():
#     if not session.get("admin_logged_in"):
#         return redirect(url_for("admin_routes.admin_login"))
#     return render_template("admin/dashboard.html", title="Admin Dashboard")

