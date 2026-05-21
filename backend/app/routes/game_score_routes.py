from flask import Blueprint, request

from app.extensions import db

from app.models.event import Event
from app.models.game import Game
from app.models.team import Team
from app.models.game_score import GameScore

from app.utils.responses import (
    success_response,
    error_response
)


game_score_bp = Blueprint(
    'game_score_bp',
    __name__
)


def _parse_score_payload(payload):
    total_score = payload.get('total_score')
    if total_score is None:
        total_score = payload.get('score_value')

    rank_position = payload.get('rank_position')
    if rank_position == '':
        rank_position = None

    is_winner = payload.get('is_winner')
    if is_winner is None:
        is_winner = payload.get('isWinner', False)

    return total_score, rank_position, is_winner


@game_score_bp.route(
    '/events/<int:event_id>/scores',
    methods=['GET']
)
def get_event_scores(event_id):
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

        data = [score.to_dict() for score in scores]

        return success_response(
            data=data,
            message='Scores fetched successfully.'
        )

    except Exception as e:
        return error_response(
            message='Failed to fetch scores.',
            errors=[str(e)],
            status_code=500
        )


@game_score_bp.route(
    '/games/<int:game_id>/scores',
    methods=['GET']
)
def get_game_scores(game_id):
    try:
        game = Game.query.get(game_id)

        if not game:
            return error_response(
                message='Game not found.',
                status_code=404
            )

        scores = GameScore.query.filter_by(
            game_id=game_id
        ).all()

        data = [score.to_dict() for score in scores]

        return success_response(
            data=data,
            message='Scores fetched successfully.'
        )

    except Exception as e:
        return error_response(
            message='Failed to fetch scores.',
            errors=[str(e)],
            status_code=500
        )


@game_score_bp.route(
    '/games/<int:game_id>/scores',
    methods=['POST']
)
def create_or_update_game_score(game_id):
    try:
        game = Game.query.get(game_id)

        if not game:
            return error_response(
                message='Game not found.',
                status_code=404
            )

        payload = request.get_json()

        if not payload:
            return error_response(
                message='Request body is required.',
                status_code=400
            )

        event_id = payload.get('event_id') or game.event_id
        team_id = payload.get('team_id')
        total_score, rank_position, is_winner = _parse_score_payload(payload)

        validation_errors = {}

        if not team_id:
            validation_errors['team_id'] = ['Team is required.']

        if total_score is None:
            validation_errors['total_score'] = ['Score value is required.']

        if validation_errors:
            return error_response(
                message='Validation failed.',
                errors=validation_errors,
                status_code=400
            )

        if int(event_id) != int(game.event_id):
            return error_response(
                message='Event does not match this game.',
                status_code=400
            )

        team = Team.query.filter_by(
            team_id=team_id,
            event_id=event_id
        ).first()

        if not team:
            return error_response(
                message='Invalid team for this event.',
                status_code=400
            )

        game_score = GameScore.query.filter_by(
            game_id=game_id,
            team_id=team_id
        ).first()

        if game_score:
            game_score.total_score = float(total_score)
            game_score.rank_position = rank_position
            game_score.is_winner = bool(is_winner)
            message = 'Score updated successfully.'
            status_code = 200
        else:
            game_score = GameScore(
                event_id=event_id,
                game_id=game_id,
                team_id=team_id,
                total_score=float(total_score),
                rank_position=rank_position,
                is_winner=bool(is_winner)
            )
            db.session.add(game_score)
            message = 'Score submitted successfully.'
            status_code = 201

        db.session.commit()

        return success_response(
            data=game_score.to_dict(),
            message=message,
            status_code=status_code
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Failed to save score.',
            errors=[str(e)],
            status_code=500
        )


@game_score_bp.route(
    '/scores/<int:score_id>',
    methods=['PUT']
)
def update_game_score(score_id):
    try:
        score = GameScore.query.get(score_id)

        if not score:
            return error_response(
                message='Score not found.',
                status_code=404
            )

        payload = request.get_json()

        if not payload:
            return error_response(
                message='Request body is required.',
                status_code=400
            )

        total_score, rank_position, is_winner = _parse_score_payload(payload)

        if total_score is not None:
            score.total_score = float(total_score)

        if 'rank_position' in payload:
            score.rank_position = rank_position

        if 'is_winner' in payload or 'isWinner' in payload:
            score.is_winner = bool(is_winner)

        db.session.commit()

        return success_response(
            data=score.to_dict(),
            message='Score updated successfully.'
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Failed to update score.',
            errors=[str(e)],
            status_code=500
        )


@game_score_bp.route(
    '/scores/<int:score_id>',
    methods=['DELETE']
)
def delete_game_score(score_id):
    try:
        score = GameScore.query.get(score_id)

        if not score:
            return error_response(
                message='Score not found.',
                status_code=404
            )

        db.session.delete(score)
        db.session.commit()

        return success_response(
            message='Score deleted successfully.'
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Failed to delete score.',
            errors=[str(e)],
            status_code=500
        )
