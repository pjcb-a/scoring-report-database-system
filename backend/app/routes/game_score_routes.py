from flask import Blueprint

from app.extensions import db
from app.models.game import Game
from app.models.game_score import GameScore
from app.models.team import Team
from app.routes.utils import (
    error_response,
    missing_fields,
    parse_bool,
    parse_float,
    parse_int,
    request_data,
    success_response
)


game_score_bp = Blueprint("game_score_bp", __name__)


@game_score_bp.route("/api/game-scores", methods=["GET"])
def get_game_scores():
    scores = GameScore.query.order_by(GameScore.game_score_id.desc()).all()

    return success_response(
        [score.to_dict() for score in scores],
        "Game scores fetched successfully."
    )


@game_score_bp.route("/api/game-scores/<int:game_score_id>", methods=["GET"])
def get_game_score(game_score_id):
    score = GameScore.query.get(game_score_id)

    if not score:
        return error_response("Game score not found.", 404)

    return success_response(
        score.to_dict(),
        "Game score fetched successfully."
    )


@game_score_bp.route("/api/games/<int:game_id>/scores", methods=["GET"])
def get_scores_by_game(game_id):
    game = Game.query.get(game_id)

    if not game:
        return error_response("Game not found.", 404)

    scores = GameScore.query.filter_by(game_id=game_id).all()

    return success_response(
        [score.to_dict() for score in scores],
        "Game scores fetched successfully."
    )


@game_score_bp.route("/api/game-scores", methods=["POST"])
def create_game_score():
    data = request_data()
    missing = missing_fields(data, ["game_id", "team_id", "score_value"])

    if missing:
        return error_response("Required fields are missing.", 400, missing)

    game_id, game_error = parse_int(data["game_id"], "game_id")
    team_id, team_error = parse_int(data["team_id"], "team_id")
    score_value, score_error = parse_float(
        data["score_value"],
        "score_value"
    )
    errors = [
        error
        for error in [game_error, team_error, score_error]
        if error
    ]

    if "rank_position" in data and data.get("rank_position") not in [None, ""]:
        rank_position, rank_error = parse_int(
            data["rank_position"],
            "rank_position"
        )

        if rank_error:
            errors.append(rank_error)
    else:
        rank_position = None

    if errors:
        return error_response("Invalid game score data.", 400, errors)

    if score_value < 0:
        return error_response("score_value cannot be negative.", 400)

    if rank_position is not None and rank_position <= 0:
        return error_response("rank_position must be greater than zero.", 400)

    if not Game.query.get(game_id):
        return error_response("Game not found.", 404)

    if not Team.query.get(team_id):
        return error_response("Team not found.", 404)

    existing_score = GameScore.query.filter_by(
        game_id=game_id,
        team_id=team_id
    ).first()

    if existing_score:
        return error_response(
            "This team already has a score for this game.",
            409
        )

    game_score = GameScore(
        game_id=game_id,
        team_id=team_id,
        score_value=score_value,
        rank_position=rank_position,
        isWinner=parse_bool(data.get("isWinner", False))
    )

    db.session.add(game_score)
    db.session.commit()

    return success_response(
        game_score.to_dict(),
        "Game score created successfully.",
        201
    )


@game_score_bp.route("/api/game-scores/<int:game_score_id>", methods=["PUT"])
def update_game_score(game_score_id):
    game_score = GameScore.query.get(game_score_id)

    if not game_score:
        return error_response("Game score not found.", 404)

    data = request_data()

    if "game_id" in data or "team_id" in data:
        game_id = game_score.game_id
        team_id = game_score.team_id

        if "game_id" in data:
            game_id, error = parse_int(data["game_id"], "game_id")

            if error:
                return error_response(
                    "Invalid game score data.",
                    400,
                    [error]
                )

            if not Game.query.get(game_id):
                return error_response("Game not found.", 404)

        if "team_id" in data:
            team_id, error = parse_int(data["team_id"], "team_id")

            if error:
                return error_response(
                    "Invalid game score data.",
                    400,
                    [error]
                )

            if not Team.query.get(team_id):
                return error_response("Team not found.", 404)

        existing_score = GameScore.query.filter(
            GameScore.game_id == game_id,
            GameScore.team_id == team_id,
            GameScore.game_score_id != game_score_id
        ).first()

        if existing_score:
            return error_response(
                "This team already has a score for this game.",
                409
            )

        game_score.game_id = game_id
        game_score.team_id = team_id

    if "score_value" in data:
        score_value, error = parse_float(data["score_value"], "score_value")

        if error:
            return error_response("Invalid game score data.", 400, [error])

        if score_value < 0:
            return error_response("score_value cannot be negative.", 400)

        game_score.score_value = score_value

    if "rank_position" in data:
        if data.get("rank_position") in [None, ""]:
            game_score.rank_position = None
        else:
            rank_position, error = parse_int(
                data["rank_position"],
                "rank_position"
            )

            if error:
                return error_response(
                    "Invalid game score data.",
                    400,
                    [error]
                )

            if rank_position <= 0:
                return error_response(
                    "rank_position must be greater than zero.",
                    400
                )

            game_score.rank_position = rank_position

    if "isWinner" in data:
        game_score.isWinner = parse_bool(data["isWinner"])

    db.session.commit()

    return success_response(
        game_score.to_dict(),
        "Game score updated successfully."
    )


@game_score_bp.route(
    "/api/game-scores/<int:game_score_id>",
    methods=["DELETE"]
)
def delete_game_score(game_score_id):
    game_score = GameScore.query.get(game_score_id)

    if not game_score:
        return error_response("Game score not found.", 404)

    db.session.delete(game_score)
    db.session.commit()

    return success_response(
        {"game_score_id": game_score_id},
        "Game score deleted successfully."
    )
