from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request
from flask import redirect
from flask import url_for

from models import db
from models.trek import Trek
from models.booking import Booking

staff = Blueprint("staff", __name__)

@staff.route("/staff")
@login_required
def dashboard():

    treks = Trek.query.filter_by(
        staff_id=current_user.id
    ).all()

    return render_template(
        "staff/dashboard.html",
        treks=treks
    )

@staff.route("/staff/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_trek(id):

    trek = Trek.query.get_or_404(id)

    if trek.staff_id != current_user.id:
        return "Unauthorized", 403

    if request.method == "POST":

        trek.slots = int(request.form["slots"])
        trek.status = request.form["status"]
        db.session.commit()

        return redirect(url_for("staff.dashboard"))

    return render_template(
        "staff/update_trek.html",
        trek=trek
    )

@staff.route("/staff/participants/<int:trek_id>")
@login_required
def participants(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.staff_id != current_user.id:
        return "Unauthorized", 403

    bookings = Booking.query.filter_by(
        trek_id=trek.id,
        status="Booked"
    ).all()

    return render_template(
        "staff/participants.html",
        trek=trek,
        bookings=bookings
    )