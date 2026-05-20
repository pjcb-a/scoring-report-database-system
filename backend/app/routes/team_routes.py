from flask import Blueprint

from app.extensions import db

from app.models.event import Event
from app.models.team import Team

from app.routes.utils import (

    clean_string,

    error_response,

    missing_fields,

    parse_int,

    request_data,

    success_response
)


team_bp = Blueprint(

    "team_bp",

    __name__
)


"""
------------------------------------------------------------------------------
GET TEAMS OF EVENT
------------------------------------------------------------------------------
"""

@team_bp.route(

    "/api/events/<int:event_id>/teams",

    methods=["GET"]
)
def get_teams_by_event(event_id):

    event = Event.query.get(event_id)

    if not event:

        return error_response(

            "Event not found.",

            404
        )

    teams = Team.query.filter_by(

        event_id=event_id

    ).all()

    return success_response(

        [team.to_dict() for team in teams],

        "Teams fetched successfully."
    )


"""
------------------------------------------------------------------------------
GET SINGLE TEAM
------------------------------------------------------------------------------
"""

@team_bp.route(

    "/api/teams/<int:team_id>",

    methods=["GET"]
)
def get_team(team_id):

    team = Team.query.get(team_id)

    if not team:

        return error_response(

            "Team not found.",

            404
        )

    return success_response(

        team.to_dict(),

        "Team fetched successfully."
    )


"""
------------------------------------------------------------------------------
CREATE TEAM INSIDE EVENT
------------------------------------------------------------------------------
"""

@team_bp.route(

    "/api/events/<int:event_id>/teams",

    methods=["POST"]
)
def create_team(event_id):

    event = Event.query.get(event_id)

    if not event:

        return error_response(

            "Event not found.",

            404
        )

    data = request_data()

    missing = missing_fields(

        data,

        [

            "team_name",

            "team_color"
        ]
    )

    if missing:

        return error_response(

            "Required fields are missing.",

            400,

            missing
        )

    team_name = clean_string(
        data["team_name"]
    )

    team_color = clean_string(
        data["team_color"]
    )

    """
    --------------------------------------------------------------------------
    DUPLICATE TEAM CHECK
    --------------------------------------------------------------------------
    """

    existing = Team.query.filter_by(

        event_id=event_id,

        team_name=team_name

    ).first()

    if existing:

        return error_response(

            "Team already exists in this event.",

            409
        )

    """
    --------------------------------------------------------------------------
    CREATE TEAM
    --------------------------------------------------------------------------
    """

    team = Team(

        event_id=event_id,

        team_name=team_name,

        team_color=team_color
    )

    db.session.add(team)

    db.session.commit()

    return success_response(

        team.to_dict(),

        "Team created successfully.",

        201
    )


"""
------------------------------------------------------------------------------
UPDATE TEAM
------------------------------------------------------------------------------
"""

@team_bp.route(

    "/api/teams/<int:team_id>",

    methods=["PUT"]
)
def update_team(team_id):

    team = Team.query.get(team_id)

    if not team:

        return error_response(

            "Team not found.",

            404
        )

    data = request_data()

    if "team_name" in data:

        team_name = clean_string(
            data["team_name"]
        )

        if not team_name:

            return error_response(

                "team_name is required.",

                400
            )

        team.team_name = team_name

    if "team_color" in data:

        team.team_color = clean_string(
            data["team_color"]
        )

    db.session.commit()

    return success_response(

        team.to_dict(),

        "Team updated successfully."
    )


"""
------------------------------------------------------------------------------
DELETE TEAM
------------------------------------------------------------------------------
"""

@team_bp.route(

    "/api/teams/<int:team_id>",

    methods=["DELETE"]
)
def delete_team(team_id):

    team = Team.query.get(team_id)

    if not team:

        return error_response(

            "Team not found.",

            404
        )

    db.session.delete(team)

    db.session.commit()

    return success_response(

        {"team_id": team_id},

        "Team deleted successfully."
    )