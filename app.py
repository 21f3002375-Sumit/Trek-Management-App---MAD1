from flask import Flask, render_template
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from config import Config
from models import db
from models.user import User
from models.trek import Trek
from models.booking import Booking
from routes.admin import admin
from routes.auth import auth
from routes.staff import staff
from routes.user import user

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

app.config.from_object(Config)

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(admin)
app.register_blueprint(auth)
app.register_blueprint(staff)
app.register_blueprint(user)

with app.app_context():
    db.create_all()
    admin_user = User.query.filter_by(
        email="sumitgoyal18072003@gmail.com"
    ).first()
    if not admin_user:
        admin_user = User(
            name="Sumit Goyal",
            email="sumitgoyal18072003@gmail.com",
            password=generate_password_hash("admin123"),
            role="Admin",
            status="Approved"
        )
        db.session.add(admin_user)
        db.session.commit()

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)

