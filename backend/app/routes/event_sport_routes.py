from flask import Blueprint

from app.extensions import db
from app.models.event import Event
from app.models.event_sport import EventSport
from app.models.sport import Sport
from app.routes.utils import (
    clean_string,
    error_response,
    missing_fields,
    parse_datetime,
    parse_int,
    request_data,
    success_response
)


event_sport_bp = Blueprint("event_sport_bp", __name__)


@event_sport_bp.route("/api/event-sports", methods=["GET"])
def get_event_sports():
    event_sports = EventSport.query.order_by(
        EventSport.event_sport_id.desc()
    ).all()

    return success_response(
        [item.to_dict() for item in event_sports],
        "Event sports fetched successfully."
    )


@event_sport_bp.route(
    "/api/event-sports/<int:event_sport_id>",
    methods=["GET"]
)
def get_event_sport(event_sport_id):
    event_sport = EventSport.query.get(event_sport_id)

    if not event_sport:
        return error_response("Event sport not found.", 404)

    return success_response(
        event_sport.to_dict(),
        "Event sport fetched successfully."
    )


@event_sport_bp.route("/api/event-sports", methods=["POST"])
def create_event_sport():
    data = request_data()
    missing = missing_fields(data, ["event_id", "sport_id", "status"])

    if missing:
        return error_response("Required fields are missing.", 400, missing)

    event_id, event_error = parse_int(data["event_id"], "event_id")
    sport_id, sport_error = parse_int(data["sport_id"], "sport_id")
    schedule, schedule_error = parse_datetime(
        data.get("schedule"),
        "schedule"
    )
    errors = [
        error
        for error in [event_error, sport_error, schedule_error]
        if error
    ]

    if errors:
        return error_response("Invalid event sport data.", 400, errors)

    if not Event.query.get(event_id):
        return error_response("Event not found.", 404)

    if not Sport.query.get(sport_id):
        return error_response("Sport not found.", 404)

    existing = EventSport.query.filter_by(
        event_id=event_id,
        sport_id=sport_id
    ).first()

    if existing:
        return error_response(
            "This sport is already assigned to this event.",
            409
        )

    event_sport = EventSport(
        event_id=event_id,
        sport_id=sport_id,
        venue=clean_string(data.get("venue")),
        schedule=schedule,
        status=clean_string(data["status"])
    )

    db.session.add(event_sport)
    db.session.commit()

    return success_response(
        event_sport.to_dict(),
        "Event sport created successfully.",
        201
    )


@event_sport_bp.route(
    "/api/event-sports/<int:event_sport_id>",
    methods=["PUT"]
)
def update_event_sport(event_sport_id):
    event_sport = EventSport.query.get(event_sport_id)

    if not event_sport:
        return error_response("Event sport not found.", 404)

    data = request_data()
    event_id = event_sport.event_id
    sport_id = event_sport.sport_id

    if "event_id" in data:
        event_id, error = parse_int(data["event_id"], "event_id")

        if error:
            return error_response("Invalid event sport data.", 400, [error])

        if not Event.query.get(event_id):
            return error_response("Event not found.", 404)

        event_sport.event_id = event_id

    if "sport_id" in data:
        sport_id, error = parse_int(data["sport_id"], "sport_id")

        if error:
            return error_response("Invalid event sport data.", 400, [error])

        if not Sport.query.get(sport_id):
            return error_response("Sport not found.", 404)

        event_sport.sport_id = sport_id

    duplicate = EventSport.query.filter(
        EventSport.event_id == event_id,
        EventSport.sport_id == sport_id,
        EventSport.event_sport_id != event_sport_id
    ).first()

    if duplicate:
        return error_response(
            "This sport is already assigned to this event.",
            409
        )

    if "venue" in data:
        event_sport.venue = clean_string(data.get("venue"))

    if "schedule" in data:
        schedule, error = parse_datetime(data.get("schedule"), "schedule")

        if error:
            return error_response("Invalid event sport data.", 400, [error])

        event_sport.schedule = schedule

    if "status" in data:
        status = clean_string(data["status"])

        if not status:
            return error_response("status is required.", 400)

        event_sport.status = status

    db.session.commit()

    return success_response(
        event_sport.to_dict(),
        "Event sport updated successfully."
    )


@event_sport_bp.route(
    "/api/event-sports/<int:event_sport_id>",
    methods=["DELETE"]
)
def delete_event_sport(event_sport_id):
    event_sport = EventSport.query.get(event_sport_id)

    if not event_sport:
        return error_response("Event sport not found.", 404)

    db.session.delete(event_sport)
    db.session.commit()

    return success_response(
        {"event_sport_id": event_sport_id},
        "Event sport deleted successfully."
    )
