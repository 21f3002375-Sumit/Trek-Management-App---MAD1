from models import db
from datetime import date


class Trek(db.Model):

    __tablename__ = "treks"

    id = db.Column( db.Integer, primary_key=True)
    name = db.Column( db.String(100) , nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    duration = db.Column( db.Integer , nullable=False)
    slots = db.Column( db.Integer , nullable=False)
    start_date = db.Column( db.Date, nullable=False)
    end_date = db.Column( db.Date , nullable=False)
    status = db.Column( db.String(30), default="Open")
    staff_id = db.Column( db.Integer, db.ForeignKey("users.id"), nullable=True)