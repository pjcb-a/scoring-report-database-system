from flask import Blueprint

from sqlalchemy import desc

from app.models.event import Event
from app.models.game_score import GameScore
from app.models.game import Game
from app.models.team import Team
from app.models.event_sport import EventSport

from app.routes.utils import (

    error_response,

    success_response
)


report_bp = Blueprint(

    "report_bp",

    __name__
)


"""
------------------------------------------------------------------------------
EVENT TEAM RANKINGS
------------------------------------------------------------------------------
"""

@report_bp.route(

    "/api/events/<int:event_id>/reports/rankings",

    methods=["GET"]
)
def get_event_rankings(event_id):

    event = Event.query.get(event_id)

    if not event:

        return error_response(

            "Event not found.",

            404
        )

    """
    --------------------------------------------------------------------------
    GET SCORES
    --------------------------------------------------------------------------
    """

    scores = GameScore.query.join(

        Team

    ).join(

        Game

    ).join(

        EventSport

    ).filter(

        EventSport.event_id == event_id

    ).all()

    """
    --------------------------------------------------------------------------
    AGGREGATE TEAM SCORES
    --------------------------------------------------------------------------
    """

    rankings = {}

    for score in scores:

        team = score.team

        if not team:
            continue

        if team.team_id not in rankings:

            rankings[team.team_id] = {

                "team_id":
                team.team_id,

                "team_name":
                team.team_name,

                "team_color":
                team.team_color,

                "total_score":
                0
            }

        rankings[team.team_id][

            "total_score"

        ] += score.final_score or 0

    """
    --------------------------------------------------------------------------
    SORT RANKINGS
    --------------------------------------------------------------------------
    """

    sorted_rankings = sorted(

        rankings.values(),

        key=lambda x: x["total_score"],

        reverse=True
    )

    return success_response(

        sorted_rankings,

        "Event rankings fetched successfully."
    )