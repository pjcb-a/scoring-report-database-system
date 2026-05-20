from sqlalchemy import func

from flask import Blueprint

from app.extensions import db
from app.models.event import Event
from app.routes.utils import (
    clean_string,
    error_response,
    missing_fields,
    parse_date,
    request_data,
    success_response
)


event_bp = Blueprint("event_bp", __name__)


@event_bp.route("/api/events", methods=["GET"])
def get_events():
    events = Event.query.order_by(Event.start_day.desc()).all()

    return success_response(
        [event.to_dict() for event in events],
        "Events fetched successfully."
    )


@event_bp.route("/api/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = Event.query.get(event_id)

    if not event:
        return error_response("Event not found.", 404)

    return success_response(
        event.to_dict(),
        "Event fetched successfully."
    )


@event_bp.route("/api/events", methods=["POST"])
def create_event():
    data = request_data()
    missing = missing_fields(
        data,
        ["event_name", "start_day", "end_day", "status"]
    )

    if missing:
        return error_response("Required fields are missing.", 400, missing)

    event_name = clean_string(data["event_name"])
    status = clean_string(data["status"])
    start_day, start_error = parse_date(data["start_day"], "start_day")
    end_day, end_error = parse_date(data["end_day"], "end_day")

    errors = [error for error in [start_error, end_error] if error]

    if errors:
        return error_response("Invalid event data.", 400, errors)

    if end_day < start_day:
        return error_response(
            "end_day cannot be earlier than start_day.",
            400
        )

    existing = Event.query.filter(
        func.lower(Event.event_name) == event_name.lower()
    ).first()

    if existing:
        return error_response("Event name already exists.", 409)

    event = Event(
        event_name=event_name,
        start_day=start_day,
        end_day=end_day,
        status=status
    )

    db.session.add(event)
    db.session.commit()

    # Auto-update system title to the new event's name
    try:
        from app.routes.event_title_routes import load_event_title, save_event_title
        settings = load_event_title()
        settings["system_title"] = event_name
        save_event_title(settings)
    except Exception as e:
        # Prevent settings update error from failing the event creation
        pass

    return success_response(
        event.to_dict(),
        "Event created successfully.",
        201
    )


@event_bp.route("/api/events/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    event = Event.query.get(event_id)

    if not event:
        return error_response("Event not found.", 404)

    data = request_data()

    if "event_name" in data:
        event_name = clean_string(data["event_name"])

        if not event_name:
            return error_response("event_name is required.", 400)

        existing = Event.query.filter(
            func.lower(Event.event_name) == event_name.lower(),
            Event.event_id != event_id
        ).first()

        if existing:
            return error_response("Event name already exists.", 409)

        event.event_name = event_name

    if "start_day" in data:
        start_day, error = parse_date(data["start_day"], "start_day")

        if error:
            return error_response("Invalid event data.", 400, [error])

        event.start_day = start_day

    if "end_day" in data:
        end_day, error = parse_date(data["end_day"], "end_day")

        if error:
            return error_response("Invalid event data.", 400, [error])

        event.end_day = end_day

    if event.end_day < event.start_day:
        return error_response(
            "end_day cannot be earlier than start_day.",
            400
        )

    if "status" in data:
        status = clean_string(data["status"])

        if not status:
            return error_response("status is required.", 400)

        event.status = status

    db.session.commit()

    return success_response(
        event.to_dict(),
        "Event updated successfully."
    )


@event_bp.route("/api/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = Event.query.get(event_id)

    if not event:
        return error_response("Event not found.", 404)

    db.session.delete(event)
    db.session.commit()

    return success_response(
        {"event_id": event_id},
        "Event deleted successfully."
    )
