from datetime import date, datetime
import re

from flask import jsonify, request


def success_response(data=None, message="Success.", status=200):
    return jsonify({
        "success": True,
        "data": data,
        "message": message
    }), status


def error_response(message, status=400, errors=None):
    payload = {
        "success": False,
        "data": None,
        "message": message
    }

    if errors:
        payload["errors"] = errors

    return jsonify(payload), status


def request_data():
    return request.get_json(silent=True) or {}


def missing_fields(data, fields):
    return [
        field
        for field in fields
        if data.get(field) is None or str(data.get(field)).strip() == ""
    ]


def clean_string(value):
    if value is None:
        return None

    return str(value).strip()


def parse_int(value, field_name):
    try:
        return int(value), None
    except (TypeError, ValueError):
        return None, f"{field_name} must be a valid integer."


def parse_float(value, field_name):
    try:
        return float(value), None
    except (TypeError, ValueError):
        return None, f"{field_name} must be a valid number."


def parse_bool(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.strip().lower() in ["true", "1", "yes", "y"]

    return bool(value)


def parse_date(value, field_name):
    if isinstance(value, date) and not isinstance(value, datetime):
        return value, None

    try:
        return date.fromisoformat(str(value)), None
    except (TypeError, ValueError):
        return None, f"{field_name} must use YYYY-MM-DD format."


def parse_datetime(value, field_name):
    if value in [None, ""]:
        return None, None

    if isinstance(value, datetime):
        return value, None

    normalized = str(value).replace("Z", "+00:00")

    try:
        return datetime.fromisoformat(normalized), None
    except (TypeError, ValueError):
        return None, f"{field_name} must be a valid datetime."


def validate_hex_color(value):
    if not value or not isinstance(value, str):
        return False
    # Matches hex color codes like #FFF, #FFFF, #FFFFFF, or #FFFFFFFF
    pattern = r"^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{4}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$"
    return bool(re.match(pattern, value.strip()))

