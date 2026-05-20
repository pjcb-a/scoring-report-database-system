from flask import Blueprint

from app.extensions import db

from app.models.event_sport import EventSport
from app.models.game import Game

from app.routes.utils import (
    clean_string,
    error_response,
    missing_fields,
    parse_datetime,
    parse_int,
    request_data,
    success_response
)


game_bp = Blueprint(
    "game_bp",
    __name__
)


"""
------------------------------------------------------------------------------
GET GAMES BY EVENT
------------------------------------------------------------------------------
"""

@game_bp.route(
    "/api/events/<int:event_id>/games",
    methods=["GET"]
)
def get_games_by_event(event_id):

    games = Game.query.join(
        EventSport
    ).filter(

        EventSport.event_id == event_id

    ).order_by(
        Game.start_date.desc()
    ).all()

    return success_response(

        [game.to_dict() for game in games],

        "Games fetched successfully."
    )


"""
------------------------------------------------------------------------------
GET SINGLE GAME
------------------------------------------------------------------------------
"""

@game_bp.route(
    "/api/games/<int:game_id>",
    methods=["GET"]
)
def get_game(game_id):

    game = Game.query.get(game_id)

    if not game:

        return error_response(
            "Game not found.",
            404
        )

    return success_response(

        game.to_dict(),

        "Game fetched successfully."
    )


"""
------------------------------------------------------------------------------
CREATE GAME
------------------------------------------------------------------------------
"""

@game_bp.route(
    "/api/games",
    methods=["POST"]
)
def create_game():

    data = request_data()

    missing = missing_fields(

        data,

        [
            "event_sport_id",
            "start_date",
            "game_status"
        ]
    )

    if missing:

        return error_response(

            "Required fields are missing.",

            400,

            missing
        )

    """
    --------------------------------------------------------------------------
    VALIDATE EVENT SPORT
    --------------------------------------------------------------------------
    """

    event_sport_id, event_sport_error = parse_int(

        data["event_sport_id"],

        "event_sport_id"
    )

    start_date, start_error = parse_datetime(

        data["start_date"],

        "start_date"
    )

    end_date, end_error = parse_datetime(

        data.get("end_date"),

        "end_date"
    )

    errors = [

        error

        for error in [

            event_sport_error,
            start_error,
            end_error

        ]

        if error
    ]

    if errors:

        return error_response(

            "Invalid game data.",

            400,

            errors
        )

    """
    --------------------------------------------------------------------------
    DATE VALIDATION
    --------------------------------------------------------------------------
    """

    if end_date and end_date < start_date:

        return error_response(

            "end_date cannot be earlier than start_date.",

            400
        )

    """
    --------------------------------------------------------------------------
    ENSURE EVENT SPORT EXISTS
    --------------------------------------------------------------------------
    """

    event_sport = EventSport.query.get(
        event_sport_id
    )

    if not event_sport:

        return error_response(

            "Event sport not found.",

            404
        )

    """
    --------------------------------------------------------------------------
    CREATE GAME
    --------------------------------------------------------------------------
    """

    game = Game(

        event_sport_id=event_sport_id,

        start_date=start_date,

        end_date=end_date,

        venue_name=clean_string(
            data.get("venue_name")
        ),

        game_status=clean_string(
            data["game_status"]
        ),

        round=clean_string(
            data.get("round")
        )
    )

    db.session.add(game)

    db.session.commit()

    return success_response(

        game.to_dict(),

        "Game created successfully.",

        201
    )


"""
------------------------------------------------------------------------------
UPDATE GAME
------------------------------------------------------------------------------
"""

@game_bp.route(
    "/api/games/<int:game_id>",
    methods=["PUT"]
)
def update_game(game_id):

    game = Game.query.get(game_id)

    if not game:

        return error_response(
            "Game not found.",
            404
        )

    data = request_data()

    """
    --------------------------------------------------------------------------
    EVENT SPORT
    --------------------------------------------------------------------------
    """

    if "event_sport_id" in data:

        event_sport_id, error = parse_int(

            data["event_sport_id"],

            "event_sport_id"
        )

        if error:

            return error_response(

                "Invalid game data.",

                400,

                [error]
            )

        event_sport = EventSport.query.get(
            event_sport_id
        )

        if not event_sport:

            return error_response(

                "Event sport not found.",

                404
            )

        game.event_sport_id = event_sport_id

    """
    --------------------------------------------------------------------------
    START DATE
    --------------------------------------------------------------------------
    """

    if "start_date" in data:

        start_date, error = parse_datetime(

            data["start_date"],

            "start_date"
        )

        if error:

            return error_response(

                "Invalid game data.",

                400,

                [error]
            )

        game.start_date = start_date

    """
    --------------------------------------------------------------------------
    END DATE
    --------------------------------------------------------------------------
    """

    if "end_date" in data:

        end_date, error = parse_datetime(

            data.get("end_date"),

            "end_date"
        )

        if error:

            return error_response(

                "Invalid game data.",

                400,

                [error]
            )

        game.end_date = end_date

    """
    --------------------------------------------------------------------------
    DATE VALIDATION
    --------------------------------------------------------------------------
    """

    if game.end_date and game.end_date < game.start_date:

        return error_response(

            "end_date cannot be earlier than start_date.",

            400
        )

    """
    --------------------------------------------------------------------------
    OPTIONAL FIELDS
    --------------------------------------------------------------------------
    """

    if "venue_name" in data:

        game.venue_name = clean_string(
            data.get("venue_name")
        )

    if "game_status" in data:

        game_status = clean_string(
            data["game_status"]
        )

        if not game_status:

            return error_response(

                "game_status is required.",

                400
            )

        game.game_status = game_status

    if "round" in data:

        game.round = clean_string(
            data.get("round")
        )

    db.session.commit()

    return success_response(

        game.to_dict(),

        "Game updated successfully."
    )


"""
------------------------------------------------------------------------------
DELETE GAME
------------------------------------------------------------------------------
"""

@game_bp.route(
    "/api/games/<int:game_id>",
    methods=["DELETE"]
)
def delete_game(game_id):

    game = Game.query.get(game_id)

    if not game:

        return error_response(
            "Game not found.",
            404
        )

    db.session.delete(game)

    db.session.commit()

    return success_response(

        {"game_id": game_id},

        "Game deleted successfully."
    )