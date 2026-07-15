from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models.booking import Booking
from models import db
from models.trek import Trek

user = Blueprint("user", __name__)

@user.route("/user")
@login_required
def dashboard():

    treks = Trek.query.filter_by(
        status="Open"
    ).all()

    return render_template(
        "user/dashboard.html",
        treks=treks
    )

@user.route("/user/book/<int:trek_id>")
@login_required
def book_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.status != "Open":
        flash("This trek is not open for booking.")
        return redirect(url_for("user.dashboard"))

    if trek.slots <= 0:
        flash("No slots available.")
        return redirect(url_for("user.dashboard"))

    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek.id,
        status="Booked"
    ).first()

    if existing_booking:
        flash("You have already booked this trek.")
        return redirect(url_for("user.dashboard"))

    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id
    )

    db.session.add(booking)
    trek.slots -= 1
    db.session.commit()
    flash("Trek booked successfully!")

    return redirect(url_for("user.dashboard"))

@user.route("/user/bookings")
@login_required
def my_bookings():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "user/bookings.html",
        bookings=bookings
    )

@user.route("/user/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":

        current_user.name = request.form["name"]
        current_user.phone = request.form["phone"]
        db.session.commit()
        flash("Profile updated successfully!")

        return redirect(url_for("user.profile"))

    return render_template(
        "user/profile.html"
    )