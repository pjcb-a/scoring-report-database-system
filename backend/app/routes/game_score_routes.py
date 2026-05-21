from flask import Blueprint, request

from app.extensions import db

from app.models.event import Event
from app.models.game import Game
from app.models.team import Team
from app.models.judge import Judge
from app.models.criteria import Criteria
from app.models.game_score import GameScore

from app.utils.responses import (

    success_response,

    error_response
)


game_score_bp = Blueprint(

    'game_score_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| GET SCORES BY GAME
|--------------------------------------------------------------------------
|
| Returns all scores for a specific game.
|
"""


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

        data = [

            score.to_dict()

            for score in scores
        ]

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


"""
|--------------------------------------------------------------------------
| CREATE GAME SCORE
|--------------------------------------------------------------------------
|
| Creates a score entry for a game.
|
"""


@game_score_bp.route(

    '/games/<int:game_id>/scores',

    methods=['POST']
)
def create_game_score(game_id):

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

        event_id = payload.get(
            'event_id'
        )

        team_id = payload.get(
            'team_id'
        )

        judge_id = payload.get(
            'judge_id'
        )

        criteria_id = payload.get(
            'criteria_id'
        )

        score_value = payload.get(
            'score_value'
        )

        """
        ----------------------------------------------------------------------
        VALIDATION
        ----------------------------------------------------------------------
        """

        validation_errors = {}

        if not event_id:

            validation_errors[
                'event_id'
            ] = [

                'Event is required.'
            ]

        if not team_id:

            validation_errors[
                'team_id'
            ] = [

                'Team is required.'
            ]

        if not judge_id:

            validation_errors[
                'judge_id'
            ] = [

                'Judge is required.'
            ]

        if not criteria_id:

            validation_errors[
                'criteria_id'
            ] = [

                'Criteria is required.'
            ]

        if score_value is None:

            validation_errors[
                'score_value'
            ] = [

                'Score value is required.'
            ]

        if validation_errors:

            return error_response(

                message='Validation failed.',

                errors=validation_errors,

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        VALIDATE EVENT
        ----------------------------------------------------------------------
        """

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Invalid event.',

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        VALIDATE TEAM
        ----------------------------------------------------------------------
        """

        team = Team.query.filter_by(

            team_id=team_id,

            event_id=event_id

        ).first()

        if not team:

            return error_response(

                message='Invalid team for this event.',

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        VALIDATE JUDGE
        ----------------------------------------------------------------------
        """

        judge = Judge.query.get(judge_id)

        if not judge:

            return error_response(

                message='Invalid judge.',

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        VALIDATE CRITERIA
        ----------------------------------------------------------------------
        """

        criteria = Criteria.query.get(criteria_id)

        if not criteria:

            return error_response(

                message='Invalid criteria.',

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        PREVENT DUPLICATE SCORE ENTRY
        ----------------------------------------------------------------------
        """

        existing_score = GameScore.query.filter_by(

            game_id=game_id,

            team_id=team_id,

            judge_id=judge_id,

            criteria_id=criteria_id

        ).first()

        if existing_score:

            return error_response(

                message='Score already exists for this criteria.',

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        CREATE SCORE
        ----------------------------------------------------------------------
        """

        game_score = GameScore(

            event_id=event_id,

            game_id=game_id,

            team_id=team_id,

            judge_id=judge_id,

            criteria_id=criteria_id,

            score_value=score_value
        )

        db.session.add(game_score)

        db.session.commit()

        return success_response(

            data=game_score.to_dict(),

            message='Score submitted successfully.',

            status_code=201
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to create score.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| UPDATE SCORE
|--------------------------------------------------------------------------
|
| Updates a score entry.
|
"""


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

        score.score_value = payload.get(

            'score_value',

            score.score_value
        )

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


"""
|--------------------------------------------------------------------------
| DELETE SCORE
|--------------------------------------------------------------------------
|
| Deletes a score entry.
|
"""


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