from flask import Blueprint, request

from app.extensions import db

from app.models.game import Game
from app.models.event import Event
from app.models.team import Team
from app.models.event_sport import EventSport

from app.utils.responses import (

    success_response,

    error_response
)


game_bp = Blueprint(

    'game_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| GET GAMES BY EVENT
|--------------------------------------------------------------------------
|
| Returns all games under a specific event.
|
"""


@game_bp.route(

    '/events/<int:event_id>/games',

    methods=['GET']
)
def get_event_games(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        games = Game.query.filter_by(

            event_id=event_id

        ).all()

        data = [

            game.to_dict()

            for game in games
        ]

        return success_response(

            data=data,

            message='Games fetched successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to fetch games.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| CREATE GAME
|--------------------------------------------------------------------------
|
| Creates a game under an event.
|
"""


@game_bp.route(

    '/events/<int:event_id>/games',

    methods=['POST']
)
def create_game(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        payload = request.get_json()

        if not payload:

            return error_response(

                message='Request body is required.',

                status_code=400
            )

        event_sport_id = payload.get(
            'event_sport_id'
        )

        team_a_id = payload.get(
            'team_a_id'
        )

        team_b_id = payload.get(
            'team_b_id'
        )

        game_name = payload.get(
            'game_name'
        )

        game_status = payload.get(
            'game_status',
            'Scheduled'
        )

        """
        ----------------------------------------------------------------------
        VALIDATION
        ----------------------------------------------------------------------
        """

        validation_errors = {}

        if not event_sport_id:

            validation_errors[
                'event_sport_id'
            ] = [

                'Event sport is required.'
            ]

        if not team_a_id:

            validation_errors[
                'team_a_id'
            ] = [

                'Team A is required.'
            ]

        if not team_b_id:

            validation_errors[
                'team_b_id'
            ] = [

                'Team B is required.'
            ]

        if not game_name:

            validation_errors[
                'game_name'
            ] = [

                'Game name is required.'
            ]

        if team_a_id == team_b_id:

            validation_errors[
                'teams'
            ] = [

                'Teams must be different.'
            ]

        if validation_errors:

            return error_response(

                message='Validation failed.',

                errors=validation_errors,

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        VALIDATE EVENT SPORT
        ----------------------------------------------------------------------
        """

        event_sport = EventSport.query.filter_by(

            event_sport_id=event_sport_id,

            event_id=event_id

        ).first()

        if not event_sport:

            return error_response(

                message='Invalid event sport.',

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        VALIDATE TEAMS
        ----------------------------------------------------------------------
        """

        team_a = Team.query.filter_by(

            team_id=team_a_id,

            event_id=event_id

        ).first()

        team_b = Team.query.filter_by(

            team_id=team_b_id,

            event_id=event_id

        ).first()

        if not team_a or not team_b:

            return error_response(

                message='Invalid teams for this event.',

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        CREATE GAME
        ----------------------------------------------------------------------
        """

        game = Game(

            event_id=event_id,

            event_sport_id=event_sport_id,

            team_a_id=team_a_id,

            team_b_id=team_b_id,

            game_name=game_name,

            game_status=game_status
        )

        db.session.add(game)

        db.session.commit()

        return success_response(

            data=game.to_dict(),

            message='Game created successfully.',

            status_code=201
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to create game.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| UPDATE GAME
|--------------------------------------------------------------------------
|
| Updates a game.
|
"""


@game_bp.route(

    '/games/<int:game_id>',

    methods=['PUT']
)
def update_game(game_id):

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

        game.game_name = payload.get(

            'game_name',

            game.game_name
        )

        db.session.commit()

        return success_response(

            data=game.to_dict(),

            message='Game updated successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to update game.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| DELETE GAME
|--------------------------------------------------------------------------
|
| Deletes a game.
|
"""


@game_bp.route(

    '/games/<int:game_id>',

    methods=['DELETE']
)
def delete_game(game_id):

    try:

        game = Game.query.get(game_id)

        if not game:

            return error_response(

                message='Game not found.',

                status_code=404
            )

        db.session.delete(game)

        db.session.commit()

        return success_response(

            message='Game deleted successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to delete game.',

            errors=[str(e)],

            status_code=500
        )