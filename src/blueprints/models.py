from datetime import datetime
from sqlalchemy.orm import backref
from database import db


class LinenType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class FloorImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Floor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    latest_image_id = db.Column(db.Integer, db.ForeignKey(FloorImage.id))
    has_trolley = db.Column(db.Boolean, default=False)

    latest_image = db.relationship("FloorImage", backref=backref("floor", uselist=True))

class FloorLinen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ltype_id = db.Column(db.Integer, db.ForeignKey(LinenType.id), nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey(Floor.id), nullable=False)
    quantity = db.Column(db.Integer)

    floor = db.relationship("Floor", backref=backref("floor_linen", uselist=True))
    ltype = db.relationship("LinenType", backref=backref("floor_linen", uselist=True))
