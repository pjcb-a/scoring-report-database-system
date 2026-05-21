from flask import Blueprint

from app.models.event import Event
from app.models.game import Game

from app.utils.responses import (
    success_response,
    error_response
)


report_bp = Blueprint(
    'report_bp',
    __name__
)


@report_bp.route(
    '/events/<int:event_id>/reports/matches',
    methods=['GET']
)
def get_event_match_reports(event_id):
    try:
        event = Event.query.get(event_id)

        if not event:
            return error_response(
                message='Event not found.',
                status_code=404
            )

        games = Game.query.filter_by(
            event_id=event_id,
            is_finalized=True
        ).order_by(
            Game.start_date.desc()
        ).all()

        data = [game.to_dict() for game in games]

        return success_response(
            data=data,
            message='Match reports fetched successfully.'
        )

    except Exception as e:
        return error_response(
            message='Failed to generate match reports.',
            errors=[str(e)],
            status_code=500
        )


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

        games = Game.query.filter_by(
            event_id=event_id,
            is_finalized=True
        ).all()

        data = []

        for game in games:
            for score in game.game_scores:
                entry = score.to_dict()
                entry['game_name'] = game.game_name
                entry['round'] = game.round
                entry['game_status'] = game.game_status
                entry['set_count'] = game.set_count
                entry['scoring_type'] = (
                    game.event_sport.sport.scoring_type.type
                    if game.event_sport
                    and game.event_sport.sport
                    and game.event_sport.sport.scoring_type
                    else None
                )
                data.append(entry)

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
