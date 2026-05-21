from flask import Blueprint

from sqlalchemy import func

from app.extensions import db

from app.models.event import Event
from app.models.team import Team
from app.models.game import Game
from app.models.sport import Sport
from app.models.event_sport import EventSport
from app.models.game_score import GameScore

from app.utils.responses import (

    success_response,

    error_response
)


dashboard_bp = Blueprint(

    'dashboard_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| EVENT DASHBOARD SUMMARY
|--------------------------------------------------------------------------
|
| Aggregated event dashboard data.
|
"""


@dashboard_bp.route(

    '/events/<int:event_id>/dashboard',

    methods=['GET']
)
def get_event_dashboard(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        """
        ----------------------------------------------------------------------
        TOTALS
        ----------------------------------------------------------------------
        """

        total_teams = Team.query.filter_by(

            event_id=event_id

        ).count()

        total_games = Game.query.filter_by(

            event_id=event_id

        ).count()

        total_sports = EventSport.query.filter_by(

            event_id=event_id

        ).count()

        total_scores = GameScore.query.filter_by(

            event_id=event_id

        ).count()

        """
        ----------------------------------------------------------------------
        RECENT GAMES
        ----------------------------------------------------------------------
        """

        recent_games = Game.query.filter_by(

            event_id=event_id

        ).order_by(

            Game.game_id.desc()

        ).limit(5).all()

        """
        ----------------------------------------------------------------------
        TOP TEAMS
        ----------------------------------------------------------------------
        """

        top_teams = db.session.query(

            Team.team_id,

            Team.team_name,

            func.coalesce(
                func.sum(GameScore.score_value),
                0
            ).label('total_score')

        ).outerjoin(

            GameScore,

            Team.team_id == GameScore.team_id

        ).filter(

            Team.event_id == event_id

        ).group_by(

            Team.team_id

        ).order_by(

            func.sum(
                GameScore.score_value
            ).desc()

        ).limit(5).all()

        """
        ----------------------------------------------------------------------
        FORMAT TOP TEAMS
        ----------------------------------------------------------------------
        """

        formatted_top_teams = [

            {

                'team_id':
                    team.team_id,

                'team_name':
                    team.team_name,

                'total_score':
                    float(team.total_score or 0)
            }

            for team in top_teams
        ]

        """
        ----------------------------------------------------------------------
        RESPONSE
        ----------------------------------------------------------------------
        """

        dashboard_data = {

            'statistics': {

                'total_teams':
                    total_teams,

                'total_games':
                    total_games,

                'total_sports':
                    total_sports,

                'total_scores':
                    total_scores
            },

            'recent_games': [

                game.to_dict()

                for game in recent_games
            ],

            'top_teams':
                formatted_top_teams
        }

        return success_response(

            data=dashboard_data,

            message='Dashboard loaded successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to load dashboard.',

            errors=[str(e)],

            status_code=500
        )