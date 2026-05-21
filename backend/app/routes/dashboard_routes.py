from flask import Blueprint

from app.models import (

    Event,

    Team,

    Game,

    GameScore,

    EventSport
)

from app.utils.responses import (

    success_response,

    error_response
)


dashboard_bp = Blueprint(

    'dashboard',

    __name__
)


"""
|--------------------------------------------------------------------------
| EVENT DASHBOARD SUMMARY
|--------------------------------------------------------------------------
"""


@dashboard_bp.route(

    '/events/<int:event_id>/dashboard',

    methods=['GET']
)
def get_dashboard_summary(event_id):

    try:

        """
        ----------------------------------------------------------------------
        VALIDATE EVENT
        ----------------------------------------------------------------------
        """

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        """
        ----------------------------------------------------------------------
        FETCH EVENT DATA
        ----------------------------------------------------------------------
        """

        sports = EventSport.query.filter_by(
                event_id=event_id
            ).all()

        teams = Team.query.filter_by(
                event_id=event_id
            ).all()

        games = Game.query.filter_by(
                event_id=event_id
            ).all()

        scores = GameScore.query.filter_by(

                event_id=event_id
            ).all()

        """
        ----------------------------------------------------------------------
        DASHBOARD SUMMARY
        ----------------------------------------------------------------------
        """

        summary = {

            'event':
                event.to_dict(),

            'statistics': {

                'total_sports':
                    len(sports),

                'total_teams':
                    len(teams),

                'total_games':
                    len(games),

                'total_scores':
                    len(scores)
            },

            'sports': [

                sport.to_dict()

                for sport in sports
            ],

            'games': [

                game.to_dict()

                for game in games
            ],

            'scores': [

                score.to_dict()

                for score in scores
            ]
        }

        return success_response(

            message='Dashboard loaded successfully.',

            data=summary
        )

    except Exception as error:

        return error_response(

            message='Failed to load dashboard.',

            errors=[str(error)],

            status_code=500
        )