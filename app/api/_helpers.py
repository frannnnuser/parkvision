from flask import jsonify
from functools import wraps
from werkzeug.exceptions import HTTPException


def success(data=None, status=200, **kwargs):
    body = {"ok": True}
    if data is not None:
        body["data"] = data
    body.update(kwargs)
    return jsonify(body), status


def error(message: str, status: int = 400):
    return jsonify({"ok": False, "error": message}), status


def validate_json(*required_fields):
    """Decorator: ensures request JSON exists and contains required fields."""
    from flask import request

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)
            if data is None:
                return error("Request body must be JSON", 400)
            missing = [f for f in required_fields if f not in data]
            if missing:
                return error(f"Missing fields: {', '.join(missing)}", 400)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
