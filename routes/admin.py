from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime

from models.user import User
from models.trek import Trek
from models.booking import Booking
from models import db

admin = Blueprint("admin", __name__)

@admin.route("/admin")
def dashboard():

    total_users = User.query.filter_by(role="User").count()
    total_staff = User.query.filter_by(role="Staff").count()
    total_treks = Trek.query.count()
    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings
    )

@admin.route("/admin/add-trek", methods=["GET", "POST"])
def add_trek():

    if request.method == "POST":

        trek = Trek(

            name=request.form["name"],
            location=request.form["location"],
            difficulty=request.form["difficulty"],
            duration=int(request.form["duration"]),
            slots=int(request.form["slots"]),
            start_date=datetime.strptime(request.form["start_date"],"%Y-%m-%d").date(),
            end_date=datetime.strptime(request.form["end_date"],"%Y-%m-%d").date(),
            status=request.form["status"]
        )

        db.session.add(trek)
        db.session.commit()

        return redirect(url_for("admin.view_treks"))

    return render_template("admin/add_trek.html")

@admin.route("/admin/treks")
def view_treks():

    treks = Trek.query.all()

    return render_template(
        "admin/all_treks.html",
        treks=treks
    )

@admin.route("/admin/edit/<int:id>", methods=["GET", "POST"])
def edit_trek(id):

    trek = Trek.query.get_or_404(id)

    if request.method == "POST":

        trek.name = request.form["name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = int(request.form["duration"])
        trek.slots = int(request.form["slots"])
        trek.start_date = datetime.strptime(request.form["start_date"],"%Y-%m-%d").date()
        trek.end_date = datetime.strptime(request.form["end_date"],"%Y-%m-%d").date()
        trek.status = request.form["status"]

        db.session.commit()

        return redirect(url_for("admin.view_treks"))

    return render_template(
        "admin/edit_trek.html",
        trek=trek
    )

@admin.route("/admin/delete/<int:id>")
def delete_trek(id):

    trek = Trek.query.get_or_404(id)
    db.session.delete(trek)
    db.session.commit()

    return redirect(url_for("admin.view_treks"))

@admin.route("/admin/staff")
def staff_list():

    staffs = User.query.filter_by(role="Staff").all()

    return render_template(
        "admin/staff.html",
        staffs=staffs
    )

@admin.route("/admin/approve/<int:id>")
def approve_staff(id):

    staff = User.query.get_or_404(id)
    staff.status = "Approved"
    db.session.commit()

    return redirect(url_for("admin.staff_list"))

@admin.route("/admin/blacklist/<int:id>")
def blacklist_staff(id):

    staff = User.query.get_or_404(id)
    staff.status = "Blacklisted"
    db.session.commit()

    return redirect(url_for("admin.staff_list"))

@admin.route("/admin/assign/<int:trek_id>", methods=["GET", "POST"])
def assign_staff(trek_id):

    trek = Trek.query.get_or_404(trek_id)
    staffs = User.query.filter_by(
        role="Staff",
        status="Approved"
    ).all()

    if request.method == "POST":

        trek.staff_id = request.form["staff_id"]
        db.session.commit()

        return redirect(url_for("admin.view_treks"))

    return render_template(
        "admin/assign_staff.html",
        trek=trek,
        staffs=staffs
    )

@admin.route("/admin/users")
def view_users():

    users = User.query.filter_by(role="User").all()

    return render_template(
        "admin/users.html",
        users=users
    )


@admin.route("/admin/staff")
def view_staff():

    staffs = User.query.filter_by(role="Staff").all()
    return render_template(
        "admin/staff.html",
        staffs=staffs
    )

@admin.route("/admin/bookings")
def all_bookings():

    bookings = Booking.query.all()
    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )

@admin.route("/admin/search")
def search():

    keyword = request.args.get("keyword", "")
    treks = Trek.query.filter(
        Trek.name.ilike(f"%{keyword}%")
    ).all()

    return render_template(
        "admin/search.html",
        treks=treks,
        keyword=keyword
    )

@admin.route("/admin/blacklist_user/<int:id>")
def blacklist_user(id):

    user = User.query.get_or_404(id)
    user.status = "Blacklisted"
    db.session.commit()

    return redirect(url_for("admin.view_users"))