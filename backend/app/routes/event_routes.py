from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.event import Event


event_bp = Blueprint("event_bp", __name__)


@event_bp.route("/api/events", methods=["GET"])
def get_events():

    events = Event.query.all()

    result = []

    for event in events:
        result.append({
            "event_id": event.event_id,
            "event_name": event.event_name,
            "start_day": event.start_day,
            "end_day": event.end_day,
            "status": event.status
        })

    return jsonify(result)


@event_bp.route("/api/events/<int:event_id>", methods=["GET"])
def get_event(event_id):

    event = Event.query.get_or_404(event_id)

    return jsonify({
        "event_id": event.event_id,
        "event_name": event.event_name,
        "start_day": event.start_day,
        "end_day": event.end_day,
        "status": event.status
    })


@event_bp.route("/api/events", methods=["POST"])
def create_event():

    data = request.get_json()

    event = Event(
        event_name=data["event_name"],
        start_day=data["start_day"],
        end_day=data["end_day"],
        status=data["status"]
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({
        "message": "Event created successfully"
    }), 201