import os
import json
from flask import Blueprint

from app.routes.utils import (
    clean_string,
    error_response,
    request_data,
    success_response
)

EVENT_TITLE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "event_title.json")
DEFAULT_TITLE = "Sports Reporting Database System"


def load_event_title():
    if not os.path.exists(EVENT_TITLE_FILE):
        return {"system_title": DEFAULT_TITLE}
    try:
        with open(EVENT_TITLE_FILE, "r") as f:
            data = json.load(f)
            if not data or "system_title" not in data:
                return {"system_title": DEFAULT_TITLE}
            return data
    except Exception:
        return {"system_title": DEFAULT_TITLE}


def save_event_title(settings):
    try:
        with open(EVENT_TITLE_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception:
        return False


event_title_bp = Blueprint("event_title_bp", __name__)


@event_title_bp.route("/api/event-title", methods=["GET"])
def get_event_title():
    settings = load_event_title()
    return success_response(
        settings,
        "Event title fetched successfully."
    )


@event_title_bp.route("/api/event-title", methods=["PUT"])
def update_event_title():
    data = request_data()
    settings = load_event_title()

    if "system_title" in data:
        title = clean_string(data["system_title"])
        if not title:
            return error_response("system_title is required.", 400)
        settings["system_title"] = title

    if save_event_title(settings):
        return success_response(
            settings,
            "Event title updated successfully."
        )
    else:
        return error_response("Failed to save event title.", 500)
