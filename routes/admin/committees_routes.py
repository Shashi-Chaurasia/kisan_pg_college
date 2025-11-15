import os
from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from models import db, Committee, Member
from werkzeug.utils import secure_filename

committee_routes_bp = Blueprint("committee_routes", __name__, url_prefix="/admin")

def register_routes(app):
    app.register_blueprint(committee_routes_bp)

UPLOAD_FOLDER = "static/uploads/committees"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@committee_routes_bp.route("/manage/committees", methods=["GET", "POST"])
def manage_committees():
    """Route to manage committees - List all committees."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))
    
    # Order committees by type and name for better organization
    committees = Committee.query.order_by(Committee.type, Committee.name).all()
    return render_template("admin/committee/manage_committees.html", committees=committees)

@committee_routes_bp.route("/manage/committees/edit/<int:id>", methods=["GET", "POST"])
@committee_routes_bp.route("/manage/committees/add", methods=["GET", "POST"], defaults={"id": None})
def add_or_edit_committee(id):
    """Route to add or edit a committee."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    committee = Committee.query.get(id) if id else None
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            type = request.form.get("type", "").strip()
            
            # Validation
            if not name or not type:
                flash("Committee name and type are required!", "error")
                return render_template("admin/committee/edit_committee.html", committee=committee)
            
            if committee:
                committee.name = name
                committee.type = type
            else:
                # Check for duplicate committee names
                existing = Committee.query.filter_by(name=name, type=type).first()
                if existing:
                    flash(f"A committee with the name '{name}' already exists in {type}!", "warning")
                    return render_template("admin/committee/edit_committee.html", committee=committee)
                
                committee = Committee(name=name, type=type)
                db.session.add(committee)

            db.session.commit()
            flash(f"Committee '{name}' {'updated' if id else 'added'} successfully!", "success")
            return redirect(url_for("committee_routes.manage_committees"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error saving committee: {str(e)}", "error")
            return render_template("admin/committee/edit_committee.html", committee=committee)

    return render_template("admin/committee/edit_committee.html", committee=committee)

@committee_routes_bp.route("/manage/committees/delete/<int:id>", methods=["POST"])
def delete_committee(id):
    """Route to delete a committee."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    committee = Committee.query.get_or_404(id)
    try:
        db.session.delete(committee)
        db.session.commit()
        flash("Committee deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting committee: {str(e)}", "error")

    return redirect(url_for("committee_routes.manage_committees"))

@committee_routes_bp.route("/manage/members/<int:committee_id>", methods=["GET", "POST"])
def manage_members(committee_id):
    """Route to manage members of a specific committee."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    committee = Committee.query.get_or_404(committee_id)
    members = Member.query.filter_by(committee_id=committee_id).all()
    return render_template("admin/committee/manage_members.html", committee=committee, members=members)

@committee_routes_bp.route("/manage/members/edit/<int:committee_id>/<int:id>", methods=["GET", "POST"])
@committee_routes_bp.route("/manage/members/add/<int:committee_id>", methods=["GET", "POST"], defaults={"id": None})
def add_or_edit_member(committee_id, id):
    """Route to add or edit a member of a committee."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    # Verify committee exists
    committee = Committee.query.get_or_404(committee_id)
    member = Member.query.get(id) if id else None
    
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            designation = request.form.get("designation", "").strip()
            bio = request.form.get("bio", "").strip()
            photo = request.files.get("photo")
            
            # Validation
            if not name or not designation:
                flash("Name and designation are required!", "error")
                return render_template("admin/committee/edit_member.html", member=member, committee_id=committee_id)
            
            if member:
                member.name = name
                member.designation = designation
                member.bio = bio
                if photo and photo.filename:
                    filename = secure_filename(photo.filename)
                    photo_path = os.path.join(UPLOAD_FOLDER, filename)
                    photo.save(photo_path)
                    member.photo = os.path.join("uploads/committees", filename)
            else:
                filename = secure_filename(photo.filename) if photo and photo.filename else None
                relative_photo_path = (
                    os.path.join("uploads/committees", filename) if filename else None
                )
                if photo and photo.filename:
                    photo_path = os.path.join(UPLOAD_FOLDER, filename)
                    photo.save(photo_path)
                member = Member(name=name, designation=designation, bio=bio, photo=relative_photo_path, committee_id=committee_id)
                db.session.add(member)

            db.session.commit()
            flash(f"Member '{name}' {'updated' if id else 'added'} successfully!", "success")
            return redirect(url_for("committee_routes.manage_members", committee_id=committee_id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error saving member: {str(e)}", "error")
            return render_template("admin/committee/edit_member.html", member=member, committee_id=committee_id)

    return render_template("admin/committee/edit_member.html", member=member, committee_id=committee_id)

@committee_routes_bp.route("/manage/members/delete/<int:committee_id>/<int:id>", methods=["POST"])
def delete_member(committee_id, id):
    """Route to delete a member of a committee."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_routes.admin_login"))

    member = Member.query.get_or_404(id)
    try:
        db.session.delete(member)
        db.session.commit()
        flash("Member deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting member: {str(e)}", "error")

    return redirect(url_for("committee_routes.manage_members", committee_id=committee_id))