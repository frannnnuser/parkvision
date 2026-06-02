from datetime import datetime
from .. import db


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id           = db.Column(db.Integer,     primary_key=True)
    plate        = db.Column(db.String(20),  unique=True, nullable=False, index=True)
    owner_name   = db.Column(db.String(100))
    owner_doc    = db.Column(db.String(20))
    brand        = db.Column(db.String(50))
    model        = db.Column(db.String(50))
    color        = db.Column(db.String(30))
    year         = db.Column(db.Integer)
    vehicle_type = db.Column(db.String(20),  default="car")
    authorized   = db.Column(db.Boolean,     default=True,  nullable=False)
    notes        = db.Column(db.Text)
    created_at   = db.Column(db.DateTime,    default=datetime.utcnow, nullable=False)

    records = db.relationship("ParkingRecord", back_populates="vehicle", lazy="dynamic")

    def to_dict(self):
        return {
            "id":           self.id,
            "plate":        self.plate,
            "owner_name":   self.owner_name,
            "owner_doc":    self.owner_doc,
            "brand":        self.brand,
            "model":        self.model,
            "color":        self.color,
            "year":         self.year,
            "vehicle_type": self.vehicle_type,
            "authorized":   self.authorized,
            "notes":        self.notes,
            "created_at":   self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Vehicle {self.plate}>"
