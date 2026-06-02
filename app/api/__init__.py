from .dashboard import bp as dashboard_bp
from .vehicles  import bp as vehicles_bp
from .records   import bp as records_bp
from .camera    import bp as camera_bp
from .slots     import bp as slots_bp

__all__ = ["dashboard_bp", "vehicles_bp", "records_bp", "camera_bp", "slots_bp"]
