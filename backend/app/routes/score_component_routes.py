from flask import Blueprint, request

from app.extensions import db

from app.models.event import Event
from app.models.criteria import Criteria
from app.models.game_score import GameScore
from app.models.judge import Judge
from app.models.score_component import ScoreComponent

from app.utils.responses import (
    success_response,
    error_response
)


score_component_bp = Blueprint(
    'score_component_bp',
    __name__
)


@score_component_bp.route(
    '/events/<int:event_id>/score-components',
    methods=['GET']
)
def get_event_score_components(event_id):
    try:
        event = Event.query.get(event_id)

        if not event:
            return error_response(
                message='Event not found.',
                status_code=404
            )

        components = (
            ScoreComponent.query
            .join(GameScore, ScoreComponent.game_score_id == GameScore.game_score_id)
            .filter(GameScore.event_id == event_id)
            .all()
        )

        data = [component.to_dict() for component in components]

        return success_response(
            data=data,
            message='Score components fetched successfully.'
        )

    except Exception as e:
        return error_response(
            message='Failed to fetch score components.',
            errors=[str(e)],
            status_code=500
        )


@score_component_bp.route(
    '/criteria/<int:criteria_id>/score-components',
    methods=['GET']
)
def get_score_components(criteria_id):
    try:
        criteria = Criteria.query.get(criteria_id)

        if not criteria:
            return error_response(
                message='Criteria not found.',
                status_code=404
            )

        components = ScoreComponent.query.filter_by(
            criteria_id=criteria_id
        ).all()

        data = [component.to_dict() for component in components]

        return success_response(
            data=data,
            message='Score components fetched successfully.'
        )

    except Exception as e:
        return error_response(
            message='Failed to fetch score components.',
            errors=[str(e)],
            status_code=500
        )


@score_component_bp.route(
    '/criteria/<int:criteria_id>/score-components',
    methods=['POST']
)
def create_score_component(criteria_id):
    try:
        criteria = Criteria.query.get(criteria_id)

        if not criteria:
            return error_response(
                message='Criteria not found.',
                status_code=404
            )

        payload = request.get_json()

        if not payload:
            return error_response(
                message='Request body is required.',
                status_code=400
            )

        game_score_id = payload.get('game_score_id')
        judge_id = payload.get('judge_id')
        score_value = payload.get('score_value')
        weighted_score = payload.get('weighted_score')

        validation_errors = {}

        if not game_score_id:
            validation_errors['game_score_id'] = ['Game score is required.']

        if not judge_id:
            validation_errors['judge_id'] = ['Judge is required.']

        if score_value is None:
            validation_errors['score_value'] = ['Score value is required.']

        if validation_errors:
            return error_response(
                message='Validation failed.',
                errors=validation_errors,
                status_code=400
            )

        game_score = GameScore.query.get(game_score_id)

        if not game_score:
            return error_response(
                message='Invalid game score.',
                status_code=400
            )

        judge = Judge.query.get(judge_id)

        if not judge:
            return error_response(
                message='Invalid judge.',
                status_code=400
            )

        if judge.event_id != game_score.event_id:
            return error_response(
                message='Judge does not belong to this event.',
                status_code=400
            )

        if criteria.event_sport_id != game_score.game.event_sport_id:
            return error_response(
                message='Criteria does not belong to this game sport.',
                status_code=400
            )

        existing = ScoreComponent.query.filter_by(
            game_score_id=game_score_id,
            criteria_id=criteria_id,
            judge_id=judge_id
        ).first()

        if existing:
            return error_response(
                message='Score already exists for this judge and criteria.',
                status_code=400
            )

        if weighted_score is None and criteria.percentage is not None:
            weighted_score = float(score_value) * (float(criteria.percentage) / 100)

        component = ScoreComponent(
            game_score_id=game_score_id,
            criteria_id=criteria_id,
            judge_id=judge_id,
            score_value=float(score_value),
            weighted_score=weighted_score
        )

        db.session.add(component)
        db.session.commit()

        return success_response(
            data=component.to_dict(),
            message='Score component created successfully.',
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Failed to create score component.',
            errors=[str(e)],
            status_code=500
        )


@score_component_bp.route(
    '/score-components/<int:component_id>',
    methods=['PUT']
)
def update_score_component(component_id):
    try:
        component = ScoreComponent.query.get(component_id)

        if not component:
            return error_response(
                message='Score component not found.',
                status_code=404
            )

        payload = request.get_json() or {}

        if 'score_value' in payload:
            component.score_value = float(payload['score_value'])

        if 'weighted_score' in payload:
            component.weighted_score = payload['weighted_score']

        db.session.commit()

        return success_response(
            data=component.to_dict(),
            message='Score component updated successfully.'
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Failed to update score component.',
            errors=[str(e)],
            status_code=500
        )


@score_component_bp.route(
    '/score-components/<int:component_id>',
    methods=['DELETE']
)
def delete_score_component(component_id):
    try:
        component = ScoreComponent.query.get(component_id)

        if not component:
            return error_response(
                message='Score component not found.',
                status_code=404
            )

        db.session.delete(component)
        db.session.commit()

        return success_response(
            message='Score component deleted successfully.'
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Failed to delete score component.',
            errors=[str(e)],
            status_code=500
        )
