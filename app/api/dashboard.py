from flask import Blueprint
from ..services.parking  import get_stats
from ..models.record     import ParkingRecord
from ._helpers           import success

bp = Blueprint("dashboard", __name__)


@bp.get("/stats")
def stats():
    return success(get_stats())


@bp.get("/inside")
def inside():
    records = ParkingRecord.query.filter_by(status="inside").all()
    return success([r.to_dict() for r in records])
