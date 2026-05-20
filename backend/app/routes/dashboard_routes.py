from flask import Blueprint

from app.models.event import Event
from app.models.event_sport import EventSport
from app.models.game import Game
from app.models.game_score import GameScore

from app.routes.utils import (

    error_response,

    success_response
)


dashboard_bp = Blueprint(

    "dashboard_bp",

    __name__
)


"""
------------------------------------------------------------------------------
EVENT DASHBOARD SUMMARY
------------------------------------------------------------------------------
"""

@dashboard_bp.route(

    "/api/events/<int:event_id>/dashboard",

    methods=["GET"]
)
def get_event_dashboard(event_id):

    event = Event.query.get(event_id)

    if not event:

        return error_response(

            "Event not found.",

            404
        )

    """
    --------------------------------------------------------------------------
    SPORTS
    --------------------------------------------------------------------------
    """

    sports = EventSport.query.filter_by(

        event_id=event_id

    ).all()

    """
    --------------------------------------------------------------------------
    GAMES
    --------------------------------------------------------------------------
    """

    games = Game.query.join(

        EventSport

    ).filter(

        EventSport.event_id == event_id

    ).all()

    """
    --------------------------------------------------------------------------
    SCORES
    --------------------------------------------------------------------------
    """

    scores = GameScore.query.join(

        Game

    ).join(

        EventSport

    ).filter(

        EventSport.event_id == event_id

    ).all()

    """
    --------------------------------------------------------------------------
    SUMMARY
    --------------------------------------------------------------------------
    """

    data = {

        "event": event.to_dict(),

        "sports": [
            sport.to_dict()
            for sport in sports
        ],

        "games": [
            game.to_dict()
            for game in games
        ],

        "scores": [
            score.to_dict()
            for score in scores
        ],

        "statistics": {

            "total_sports":
            len(sports),

            "total_games":
            len(games),

            "total_scores":
            len(scores)
        }
    }

    return success_response(

        data,

        "Dashboard summary fetched successfully."
    )