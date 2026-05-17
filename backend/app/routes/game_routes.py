from flask import Blueprint, jsonify

from app.models.game import Game


game_bp = Blueprint("game_bp", __name__)


@game_bp.route("/api/games", methods=["GET"])
def get_games():

    games = Game.query.all()

    result = []

    for game in games:
        result.append({
            "game_id": game.game_id,
            "round": game.round,
            "status": game.status
        })

    return jsonify(result)