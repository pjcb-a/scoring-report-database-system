from flask import Blueprint

from sqlalchemy import func

from app.models.event import Event
from app.models.team import Team
from app.models.game_score import GameScore

from app.utils.responses import (

    success_response,

    error_response
)


report_bp = Blueprint(

    'report_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| EVENT RANKINGS REPORT
|--------------------------------------------------------------------------
|
| Returns rankings for an event.
|
"""


@report_bp.route(

    '/events/<int:event_id>/reports/rankings',

    methods=['GET']
)
def get_event_rankings(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        rankings = db.session.query(

            Team.team_id,

            Team.team_name,

            Team.team_color,

            func.coalesce(

                func.sum(
                    GameScore.score_value
                ),

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

        ).all()

        formatted_rankings = [

            {

                'team_id':
                    ranking.team_id,

                'team_name':
                    ranking.team_name,

                'team_color':
                    ranking.team_color,

                'total_score':
                    float(
                        ranking.total_score or 0
                    )
            }

            for ranking in rankings
        ]

        return success_response(

            data=formatted_rankings,

            message='Rankings fetched successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to generate rankings.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| EVENT SCORE SUMMARY
|--------------------------------------------------------------------------
|
| Returns scoring summary for reports.
|
"""


@report_bp.route(

    '/events/<int:event_id>/reports/scores',

    methods=['GET']
)
def get_event_scores_report(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        scores = GameScore.query.filter_by(

            event_id=event_id

        ).all()

        data = [

            score.to_dict()

            for score in scores
        ]

        return success_response(

            data=data,

            message='Score report generated successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to generate score report.',

            errors=[str(e)],

            status_code=500
        )