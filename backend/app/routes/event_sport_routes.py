from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.event_sport import EventSport


event_sport_bp = Blueprint("event_sport_bp", __name__)


@event_sport_bp.route("/api/event-sports", methods=["GET"])
def get_event_sports():

    event_sports = EventSport.query.all()

    result = []

    for item in event_sports:
        result.append({
            "event_sport_id": item.event_sport_id,
            "event_name": item.event.event_name,
            "sport_name": item.sport.sport_name,
            "venue": item.venue,
            "status": item.status
        })

    return jsonify(result)


@event_sport_bp.route("/api/event-sports", methods=["POST"])
def create_event_sport():

    data = request.get_json()

    event_sport = EventSport(
        event_id=data["event_id"],
        sport_id=data["sport_id"],
        venue=data.get("venue"),
        schedule=data.get("schedule"),
        status=data.get("status")
    )

    db.session.add(event_sport)
    db.session.commit()

    return jsonify({
        "message": "Event sport created successfully"
    }), 201