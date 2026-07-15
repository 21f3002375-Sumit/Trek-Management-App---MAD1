from datetime import datetime
from models import db

class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column( db.Integer,primary_key=True)
    user_id = db.Column( db.Integer,db.ForeignKey("users.id"))
    trek_id = db.Column( db.Integer, db.ForeignKey("treks.id"))
    booking_date = db.Column( db.DateTime, default=datetime.utcnow)
    status = db.Column( db.String(20), default="Booked")
    user = db.relationship("User", backref="bookings")
    trek = db.relationship("Trek", backref="bookings")