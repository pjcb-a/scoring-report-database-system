from flask import Blueprint, request

from app.extensions import db

from app.models.game import Game
from app.models.game_score import GameScore
from app.models.event import Event
from app.models.event_sport import EventSport
from app.models.team import Team


ALLOWED_GAME_STATUSES = {
    'Win',
    'Forfeit',
    'Suspensions'
}

from app.routes.utils import (
    parse_datetime,
    clean_string
)

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

        game_name = clean_string(
            payload.get('game_name')
        )

        game_status = clean_string(
            payload.get(
                'game_status',
                'Win'
            )
        ) or 'Win'

        team_ids_raw = payload.get(
            'team_ids',
            []
        )

        round_name = clean_string(
            payload.get('round')
        )

        venue_name = clean_string(
            payload.get('venue_name')
            or payload.get('venue')
        )

        start_raw = (
            payload.get('start_date')
            or payload.get('start_time')
        )

        end_raw = (
            payload.get('end_date')
            or payload.get('end_time')
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

        if game_status not in ALLOWED_GAME_STATUSES:

            validation_errors[
                'game_status'
            ] = [

                'Game status must be Win, Forfeit, or Suspensions.'
            ]

        if not isinstance(team_ids_raw, list):

            validation_errors[
                'team_ids'
            ] = [

                'Teams must be provided as a list.'
            ]

        team_ids = []

        if isinstance(team_ids_raw, list):

            for team_id in team_ids_raw:

                try:

                    team_ids.append(int(team_id))

                except (TypeError, ValueError):

                    validation_errors[
                        'team_ids'
                    ] = [

                        'Each team id must be a valid integer.'
                    ]

                    break

            team_ids = list(dict.fromkeys(team_ids))

        if not team_ids:

            validation_errors[
                'team_ids'
            ] = [

                'Select at least one team for this game.'
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

        validated_teams = []

        for team_id in team_ids:

            team = Team.query.filter_by(

                team_id=team_id,

                event_id=event_id

            ).first()

            if not team:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'team_ids': [
                            f'Team {team_id} is not part of this event.'
                        ]
                    },

                    status_code=400
                )

            validated_teams.append(team)

        start_date, start_error = parse_datetime(
            start_raw,
            'Start time'
        )

        if start_error:

            return error_response(

                message='Validation failed.',

                errors={
                    'start_time': [start_error]
                },

                status_code=400
            )

        end_date, end_error = parse_datetime(
            end_raw,
            'End time'
        )

        if end_error:

            return error_response(

                message='Validation failed.',

                errors={
                    'end_time': [end_error]
                },

                status_code=400
            )

        if not game_name:

            sport_label = (
                event_sport.sport.sport_name
                if event_sport.sport
                else 'Game'
            )

            game_name = (
                f"{sport_label} - {round_name}"
                if round_name
                else sport_label
            )

        """
        ----------------------------------------------------------------------
        CREATE GAME
        ----------------------------------------------------------------------
        """

        game = Game(

            event_id=event_id,

            event_sport_id=event_sport_id,

            game_name=game_name,

            start_date=start_date,

            end_date=end_date,

            venue_name=venue_name,

            game_status=game_status,

            round=round_name
        )

        db.session.add(game)

        db.session.flush()

        for team in validated_teams:

            db.session.add(

                GameScore(

                    event_id=event_id,

                    game_id=game.game_id,

                    team_id=team.team_id,

                    total_score=0,

                    is_winner=False
                )
            )

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

        if 'game_name' in payload:

            game.game_name = clean_string(
                payload.get('game_name')
            ) or game.game_name

        if 'event_sport_id' in payload:

            event_sport_id = payload.get(
                'event_sport_id'
            )

            event_sport = EventSport.query.filter_by(

                event_sport_id=event_sport_id,

                event_id=game.event_id

            ).first()

            if not event_sport:

                return error_response(

                    message='Invalid event sport.',

                    status_code=400
                )

            game.event_sport_id = event_sport_id

        start_raw = (
            payload.get('start_date')
            if 'start_date' in payload
            else payload.get('start_time')
            if 'start_time' in payload
            else None
        )

        if start_raw is not None:

            start_date, start_error = parse_datetime(
                start_raw,
                'Start time'
            )

            if start_error:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'start_time': [start_error]
                    },

                    status_code=400
                )

            game.start_date = start_date

        end_raw = (
            payload.get('end_date')
            if 'end_date' in payload
            else payload.get('end_time')
            if 'end_time' in payload
            else None
        )

        if end_raw is not None:

            end_date, end_error = parse_datetime(
                end_raw,
                'End time'
            )

            if end_error:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'end_time': [end_error]
                    },

                    status_code=400
                )

            game.end_date = end_date

        if 'venue_name' in payload or 'venue' in payload:

            game.venue_name = clean_string(
                payload.get('venue_name')
                or payload.get('venue')
            )

        if 'game_status' in payload:

            next_status = clean_string(
                payload.get('game_status')
            ) or game.game_status

            if next_status not in ALLOWED_GAME_STATUSES:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'game_status': [
                            'Game status must be Win, Forfeit, or Suspensions.'
                        ]
                    },

                    status_code=400
                )

            game.game_status = next_status

        if 'round' in payload:

            game.round = clean_string(
                payload.get('round')
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