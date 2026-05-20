from sqlalchemy import func

from flask import Blueprint

from app.extensions import db

from app.models.event import Event
from app.models.event_sport import EventSport
from app.models.scoring_type import ScoringType
from app.models.sport import Sport

from app.routes.utils import (
    clean_string,
    error_response,
    missing_fields,
    parse_int,
    request_data,
    success_response
)


sport_bp = Blueprint(
    "sport_bp",
    __name__
)


"""
------------------------------------------------------------------------------
GLOBAL SPORTS
MASTER SPORT TYPES
------------------------------------------------------------------------------
"""

@sport_bp.route(
    "/api/sports",
    methods=["GET"]
)
def get_sports():

    sports = Sport.query.order_by(
        Sport.sport_name.asc()
    ).all()

    return success_response(

        [sport.to_dict() for sport in sports],

        "Sports fetched successfully."
    )


"""
------------------------------------------------------------------------------
GET SPORTS OF EVENT
------------------------------------------------------------------------------
"""

@sport_bp.route(
    "/api/events/<int:event_id>/sports",
    methods=["GET"]
)
def get_sports_by_event(event_id):

    event_sports = EventSport.query.filter_by(

        event_id=event_id

    ).all()

    return success_response(

        [
            event_sport.to_dict()
            for event_sport in event_sports
        ],

        "Event sports fetched successfully."
    )


"""
------------------------------------------------------------------------------
CREATE GLOBAL SPORT
------------------------------------------------------------------------------
"""

@sport_bp.route(
    "/api/sports",
    methods=["POST"]
)
def create_sport():

    data = request_data()

    missing = missing_fields(

        data,

        [
            "sport_name",
            "scoring_type_id"
        ]
    )

    if missing:

        return error_response(

            "Required fields are missing.",

            400,

            missing
        )

    sport_name = clean_string(
        data["sport_name"]
    )

    scoring_type_id, error = parse_int(

        data["scoring_type_id"],

        "scoring_type_id"
    )

    if error:

        return error_response(

            "Invalid sport data.",

            400,

            [error]
        )

    scoring_type = ScoringType.query.get(
        scoring_type_id
    )

    if not scoring_type:

        return error_response(

            "Scoring type not found.",

            404
        )

    existing = Sport.query.filter(

        func.lower(Sport.sport_name)
        == sport_name.lower()

    ).first()

    if existing:

        return error_response(

            "Sport name already exists.",

            409
        )

    sport = Sport(

        sport_name=sport_name,

        scoring_type_id=scoring_type_id
    )

    db.session.add(sport)

    db.session.commit()

    return success_response(

        sport.to_dict(),

        "Sport created successfully.",

        201
    )


"""
------------------------------------------------------------------------------
ADD SPORT TO EVENT
------------------------------------------------------------------------------
"""

@sport_bp.route(
    "/api/events/<int:event_id>/sports",
    methods=["POST"]
)
def add_sport_to_event(event_id):

    event = Event.query.get(event_id)

    if not event:

        return error_response(
            "Event not found.",
            404
        )

    data = request_data()

    missing = missing_fields(
        data,
        ["sport_id"]
    )

    if missing:

        return error_response(
            "Required fields are missing.",
            400,
            missing
        )

    sport_id, error = parse_int(
        data["sport_id"],
        "sport_id"
    )

    if error:

        return error_response(
            "Invalid sport data.",
            400,
            [error]
        )

    sport = Sport.query.get(sport_id)

    if not sport:

        return error_response(
            "Sport not found.",
            404
        )

    existing = EventSport.query.filter_by(

        event_id=event_id,

        sport_id=sport_id

    ).first()

    if existing:

        return error_response(

            "Sport already exists in this event.",

            409
        )

    event_sport = EventSport(

        event_id=event_id,

        sport_id=sport_id
    )

    db.session.add(event_sport)

    db.session.commit()

    return success_response(

        event_sport.to_dict(),

        "Sport added to event successfully.",

        201
    )


"""
------------------------------------------------------------------------------
DELETE EVENT SPORT
------------------------------------------------------------------------------
"""

@sport_bp.route(
    "/api/event-sports/<int:event_sport_id>",
    methods=["DELETE"]
)
def delete_event_sport(event_sport_id):

    event_sport = EventSport.query.get(
        event_sport_id
    )

    if not event_sport:

        return error_response(
            "Event sport not found.",
            404
        )

    db.session.delete(event_sport)

    db.session.commit()

    return success_response(

        {"event_sport_id": event_sport_id},

        "Event sport removed successfully."
    )