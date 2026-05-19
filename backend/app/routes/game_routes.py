from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.game import Game


game_bp = Blueprint(
    "game_bp",
    __name__
)


"""
------------------------------------------------------------------------------
GET ALL GAMES
------------------------------------------------------------------------------
"""

@game_bp.route(
    "/api/games",
    methods=["GET"]
)
def get_games():

    games = Game.query.all()

    result = []

    for game in games:

        result.append({

            "game_id":
            game.game_id,

            "event":
            game.event_sport.event.event_name,

            "sport":
            game.event_sport.sport.sport_name,

            "start_date":
            game.start_date,

            "end_date":
            game.end_date,

            "venue_name":
            game.venue_name,

            "game_status":
            game.game_status,

            "round":
            game.round
        })

    return jsonify(result)


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

    data = request.get_json()

    game = Game(

        event_sport_id=
        data["event_sport_id"],

        start_date=
        data["start_date"],

        end_date=
        data.get("end_date"),

        venue_name=
        data.get("venue_name"),

        game_status=
        data["game_status"],

        round=
        data.get("round")
    )

    db.session.add(game)

    db.session.commit()

    return jsonify({

        "message":
        "Game created successfully"
    }), 201


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

    game = Game.query.get_or_404(
        game_id
    )

    data = request.get_json()

    game.start_date = data.get(
        "start_date",
        game.start_date
    )

    game.end_date = data.get(
        "end_date",
        game.end_date
    )

    game.venue_name = data.get(
        "venue_name",
        game.venue_name
    )

    game.game_status = data.get(
        "game_status",
        game.game_status
    )

    game.round = data.get(
        "round",
        game.round
    )

    db.session.commit()

    return jsonify({

        "message":
        "Game updated successfully"
    })


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

    game = Game.query.get_or_404(
        game_id
    )

    db.session.delete(game)

    db.session.commit()

    return jsonify({

        "message":
        "Game deleted successfully"
    })