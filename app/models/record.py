from datetime import datetime
from .. import db


class ParkingRecord(db.Model):
    __tablename__ = "parking_records"

    id         = db.Column(db.Integer,   primary_key=True)
    plate      = db.Column(db.String(20), nullable=False, index=True)
    vehicle_id = db.Column(db.Integer,   db.ForeignKey("vehicles.id"), nullable=True)
    slot_code  = db.Column(db.String(10))
    entry_time = db.Column(db.DateTime,  default=datetime.utcnow, nullable=False)
    exit_time  = db.Column(db.DateTime,  nullable=True)
    status     = db.Column(db.String(10), default="inside",  nullable=False)   # inside | exited
    event_type = db.Column(db.String(10), default="entry",   nullable=False)   # entry  | exit
    is_known   = db.Column(db.Boolean,   default=False,      nullable=False)
    confidence = db.Column(db.Float,     nullable=True)
    image_path = db.Column(db.String(200))
    source     = db.Column(db.String(20), default="manual")  # manual | upload | camera

    vehicle = db.relationship("Vehicle", back_populates="records")

    @property
    def duration_minutes(self):
        end = self.exit_time or datetime.utcnow()
        return int((end - self.entry_time).total_seconds() / 60)

    def to_dict(self):
        return {
            "id":               self.id,
            "plate":            self.plate,
            "slot_code":        self.slot_code,
            "entry_time":       self.entry_time.isoformat(),
            "exit_time":        self.exit_time.isoformat() if self.exit_time else None,
            "status":           self.status,
            "event_type":       self.event_type,
            "is_known":         self.is_known,
            "confidence":       self.confidence,
            "source":           self.source,
            "duration_minutes": self.duration_minutes,
            "owner_name":       self.vehicle.owner_name if self.vehicle else None,
            "vehicle":          self.vehicle.to_dict()  if self.vehicle else None,
        }

    def __repr__(self):
        return f"<ParkingRecord {self.plate} {self.event_type}>"
