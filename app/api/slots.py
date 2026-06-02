from flask import Blueprint
from ..models.slot import ParkingSlot
from ._helpers     import success

bp = Blueprint("slots", __name__)


@bp.get("/")
def list_slots():
    slots = ParkingSlot.query.order_by(ParkingSlot.level, ParkingSlot.code).all()
    return success([s.to_dict() for s in slots])
