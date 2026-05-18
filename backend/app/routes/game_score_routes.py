from flask import Blueprint, jsonify, request

from app.extensions import db

from app.models.game_score import GameScore
from app.models.game import Game
from app.models.team import Team


game_score_bp = Blueprint(
    "game_score_bp",
    __name__
)


"""
------------------------------------------------------------------------------
GET ALL GAME SCORES
------------------------------------------------------------------------------
"""

@game_score_bp.route(
    "/api/game-scores",
    methods=["GET"]
)
def get_game_scores():

    try:

        scores = GameScore.query.all()

        result = []

        for score in scores:

            result.append({

                "game_score_id":
                score.game_score_id,

                "game_id":
                score.game_id,

                "team_id":
                score.team_id,

                "team":
                score.team.team_name,

                "score_value":
                score.score_value,

                "rank_position":
                score.rank_position,

                "isWinner":
                score.isWinner
            })

        return jsonify(result), 200

    except Exception as error:

        return jsonify({
            "message":
            "Failed to fetch game scores.",

            "error":
            str(error)
        }), 500


"""
------------------------------------------------------------------------------
GET SINGLE GAME SCORE
------------------------------------------------------------------------------
"""

@game_score_bp.route(
    "/api/game-scores/<int:game_score_id>",
    methods=["GET"]
)
def get_game_score(game_score_id):

    try:

        score = GameScore.query.get_or_404(
            game_score_id
        )

        return jsonify({

            "game_score_id":
            score.game_score_id,

            "game_id":
            score.game_id,

            "team_id":
            score.team_id,

            "team":
            score.team.team_name,

            "score_value":
            score.score_value,

            "rank_position":
            score.rank_position,

            "isWinner":
            score.isWinner

        }), 200

    except Exception as error:

        return jsonify({
            "message":
            "Failed to fetch game score.",

            "error":
            str(error)
        }), 500


"""
------------------------------------------------------------------------------
GET ALL SCORES OF A GAME
------------------------------------------------------------------------------
"""

@game_score_bp.route(
    "/api/games/<int:game_id>/scores",
    methods=["GET"]
)
def get_scores_by_game(game_id):

    try:

        game = Game.query.get_or_404(game_id)

        scores = GameScore.query.filter_by(
            game_id=game.game_id
        ).all()

        result = []

        for score in scores:

            result.append({

                "game_score_id":
                score.game_score_id,

                "team_id":
                score.team_id,

                "team":
                score.team.team_name,

                "score_value":
                score.score_value,

                "rank_position":
                score.rank_position,

                "isWinner":
                score.isWinner
            })

        return jsonify(result), 200

    except Exception as error:

        return jsonify({
            "message":
            "Failed to fetch scores for game.",

            "error":
            str(error)
        }), 500


"""
------------------------------------------------------------------------------
CREATE GAME SCORE
------------------------------------------------------------------------------
"""

@game_score_bp.route(
    "/api/game-scores",
    methods=["POST"]
)
def create_game_score():

    try:

        data = request.get_json()

        """
        ----------------------------------------------------------------------
        REQUIRED FIELD VALIDATION
        ----------------------------------------------------------------------
        """

        required_fields = [
            "game_id",
            "team_id",
            "score_value"
        ]

        for field in required_fields:

            if field not in data:

                return jsonify({
                    "message":
                    f"{field} is required."
                }), 400

        """
        ----------------------------------------------------------------------
        VERIFY GAME EXISTS
        ----------------------------------------------------------------------
        """

        game = Game.query.get(
            data["game_id"]
        )

        if not game:

            return jsonify({
                "message":
                "Game not found."
            }), 404

        """
        ----------------------------------------------------------------------
        VERIFY TEAM EXISTS
        ----------------------------------------------------------------------
        """

        team = Team.query.get(
            data["team_id"]
        )

        if not team:

            return jsonify({
                "message":
                "Team not found."
            }), 404

        """
        ----------------------------------------------------------------------
        PREVENT DUPLICATE TEAM SCORE
        ----------------------------------------------------------------------
        """

        existing_score = GameScore.query.filter_by(
            game_id=data["game_id"],
            team_id=data["team_id"]
        ).first()

        if existing_score:

            return jsonify({
                "message":
                "This team already has a score "
                "for this game."
            }), 400

        """
        ----------------------------------------------------------------------
        CREATE GAME SCORE
        ----------------------------------------------------------------------
        """

        game_score = GameScore(

            game_id=data["game_id"],

            team_id=data["team_id"],

            score_value=data["score_value"],

            rank_position=data.get(
                "rank_position"
            ),

            isWinner=data.get(
                "isWinner",
                False
            )
        )

        db.session.add(game_score)

        db.session.commit()

        return jsonify({

            "message":
            "Game score created successfully.",

            "data": {

                "game_score_id":
                game_score.game_score_id,

                "game_id":
                game_score.game_id,

                "team_id":
                game_score.team_id,

                "score_value":
                game_score.score_value,

                "rank_position":
                game_score.rank_position,

                "isWinner":
                game_score.isWinner
            }

        }), 201

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message":
            "Failed to create game score.",

            "error":
            str(error)
        }), 500


"""
------------------------------------------------------------------------------
UPDATE GAME SCORE
------------------------------------------------------------------------------
"""

@game_score_bp.route(
    "/api/game-scores/<int:game_score_id>",
    methods=["PUT"]
)
def update_game_score(game_score_id):

    try:

        game_score = GameScore.query.get_or_404(
            game_score_id
        )

        data = request.get_json()

        """
        ----------------------------------------------------------------------
        UPDATE FIELDS
        ----------------------------------------------------------------------
        """

        game_score.score_value = data.get(
            "score_value",
            game_score.score_value
        )

        game_score.rank_position = data.get(
            "rank_position",
            game_score.rank_position
        )

        game_score.isWinner = data.get(
            "isWinner",
            game_score.isWinner
        )

        db.session.commit()

        return jsonify({
            "message":
            "Game score updated successfully."
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message":
            "Failed to update game score.",

            "error":
            str(error)
        }), 500


"""
------------------------------------------------------------------------------
DELETE GAME SCORE
------------------------------------------------------------------------------
"""

@game_score_bp.route(
    "/api/game-scores/<int:game_score_id>",
    methods=["DELETE"]
)
def delete_game_score(game_score_id):

    try:

        game_score = GameScore.query.get_or_404(
            game_score_id
        )

        db.session.delete(game_score)

        db.session.commit()

        return jsonify({
            "message":
            "Game score deleted successfully."
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message":
            "Failed to delete game score.",

            "error":
            str(error)
        }), 500