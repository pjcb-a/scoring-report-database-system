from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.game_score import GameScore


game_score_bp = Blueprint("game_score_bp", __name__)


@game_score_bp.route("/api/game-scores", methods=["GET"])
def get_game_scores():

    scores = GameScore.query.all()

    result = []

    for score in scores:
        result.append({
            "game_score_id": score.game_score_id,
            "team": score.team.team_name,
            "score_value": score.score_value,
            "isWinner": score.isWinner
        })

    return jsonify(result)


@game_score_bp.route("/api/game-scores", methods=["POST"])
def create_game_score():

    data = request.get_json()

    game_score = GameScore(
        game_id=data["game_id"],
        team_id=data["team_id"],
        score_value=data.get("score_value"),
        isWinner=data.get("isWinner")
    )

    db.session.add(game_score)
    db.session.commit()

    return jsonify({
        "message": "Game score created successfully"
    }), 201