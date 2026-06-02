from .. import db


class ParkingSlot(db.Model):
    __tablename__ = "parking_slots"

    id       = db.Column(db.Integer,   primary_key=True)
    code     = db.Column(db.String(10), unique=True, nullable=False)
    level    = db.Column(db.Integer,   default=1,    nullable=False)
    occupied = db.Column(db.Boolean,   default=False, nullable=False)
    plate    = db.Column(db.String(20), nullable=True)

    @classmethod
    def assign(cls, plate: str):
        slot = cls.query.filter_by(occupied=False).first()
        if slot:
            slot.occupied = True
            slot.plate    = plate
        return slot

    @classmethod
    def release(cls, plate: str):
        slot = cls.query.filter_by(plate=plate).first()
        if slot:
            slot.occupied = False
            slot.plate    = None
        return slot

    def to_dict(self):
        return {
            "id":       self.id,
            "code":     self.code,
            "level":    self.level,
            "occupied": self.occupied,
            "plate":    self.plate,
        }

    def __repr__(self):
        return f"<ParkingSlot {self.code} {'occupied' if self.occupied else 'free'}>"
