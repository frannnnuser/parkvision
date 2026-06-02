from datetime import datetime
from .. import db
from ..models.vehicle import Vehicle
from ..models.record  import ParkingRecord
from ..models.slot    import ParkingSlot


class ParkingEvent:
    def __init__(self, plate, event_type, is_known, authorized,
                 confidence, simulated, slot_code, record_id, vehicle):
        self.plate      = plate
        self.event_type = event_type
        self.is_known   = is_known
        self.authorized = authorized
        self.confidence = confidence
        self.simulated  = simulated
        self.slot_code  = slot_code
        self.record_id  = record_id
        self.vehicle    = vehicle
        self.timestamp  = datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "plate":      self.plate,
            "event_type": self.event_type,
            "is_known":   self.is_known,
            "authorized": self.authorized,
            "confidence": self.confidence,
            "simulated":  self.simulated,
            "slot_code":  self.slot_code,
            "record_id":  self.record_id,
            "timestamp":  self.timestamp,
            "vehicle": {
                "owner_name":   self.vehicle.owner_name   if self.vehicle else None,
                "brand":        self.vehicle.brand        if self.vehicle else None,
                "model":        self.vehicle.model        if self.vehicle else None,
                "color":        self.vehicle.color        if self.vehicle else None,
                "year":         self.vehicle.year         if self.vehicle else None,
                "vehicle_type": self.vehicle.vehicle_type if self.vehicle else None,
                "authorized":   self.vehicle.authorized   if self.vehicle else None,
            },
        }


def process_plate(plate, confidence=1.0, image_path=None,
                  source="manual", simulated=False):
    plate      = plate.upper().strip()
    vehicle    = Vehicle.query.filter_by(plate=plate).first()
    is_known   = vehicle is not None
    authorized = vehicle.authorized if vehicle else True
    inside     = ParkingRecord.query.filter_by(plate=plate, status="inside").first()
    event_type = "exit" if inside else "entry"
    slot_code  = None

    if event_type == "entry":
        slot      = ParkingSlot.assign(plate)
        slot_code = slot.code if slot else None
        record    = ParkingRecord(
            plate      = plate,
            vehicle_id = vehicle.id if vehicle else None,
            slot_code  = slot_code,
            event_type = "entry",
            status     = "inside",
            is_known   = is_known,
            confidence = confidence,
            image_path = image_path,
            source     = source,
        )
        db.session.add(record)
    else:
        inside.exit_time  = datetime.utcnow()
        inside.status     = "exited"
        inside.event_type = "exit"
        ParkingSlot.release(plate)
        record    = inside
        slot_code = record.slot_code

    db.session.commit()

    return ParkingEvent(
        plate      = plate,
        event_type = event_type,
        is_known   = is_known,
        authorized = authorized,
        confidence = confidence,
        simulated  = simulated,
        slot_code  = slot_code,
        record_id  = record.id,
        vehicle    = vehicle,
    )


def get_stats():
    from sqlalchemy import func
    total    = ParkingSlot.query.count()
    occupied = ParkingSlot.query.filter_by(occupied=True).count()
    today    = datetime.utcnow().date()
    return {
        "total_slots":    total,
        "occupied":       occupied,
        "free":           total - occupied,
        "entries_today":  ParkingRecord.query.filter(
            func.date(ParkingRecord.entry_time) == today
        ).count(),
        "unknown_today":  ParkingRecord.query.filter(
            func.date(ParkingRecord.entry_time) == today,
            ParkingRecord.is_known == False,
        ).count(),
        "known_vehicles": Vehicle.query.count(),
    }