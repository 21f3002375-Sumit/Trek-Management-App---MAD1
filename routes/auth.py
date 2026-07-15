from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from models import db
from models.user import User

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = generate_password_hash(request.form["password"])
        role = request.form["role"]
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered. Please use another email.")
            return redirect(url_for("auth.register"))

        status = "Pending" if role == "Staff" else "Approved"

        user = User(
            name=name,
            email=email,
            phone=phone,
            password=password,
            role=role,
            status=status
        )

        db.session.add(user)
        db.session.commit()
        flash("Registration Successful!")

        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            if user.status != "Approved":
                flash("Your account is not approved yet.")
                return redirect(url_for("auth.login"))

            login_user(user)

            if user.role == "Admin":
                return redirect(url_for("admin.dashboard"))
            elif user.role == "Staff":
                return redirect(url_for("staff.dashboard"))
            else:
                return redirect(url_for("user.dashboard"))

        flash("Invalid email or password")

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():

    logout_user()
    flash("Logged out successfully.")

    return redirect(url_for("auth.login"))