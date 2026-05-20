from flask import Blueprint

from app.extensions import db

from app.models.game import Game
from app.models.game_score import GameScore
from app.models.team import Team

from app.routes.utils import (

    error_response,

    missing_fields,

    parse_float,

    parse_int,

    request_data,

    success_response
)


game_score_bp = Blueprint(

    "game_score_bp",

    __name__
)


"""
------------------------------------------------------------------------------
GET SCORES OF GAME
------------------------------------------------------------------------------
"""

@game_score_bp.route(

    "/api/games/<int:game_id>/scores",

    methods=["GET"]
)
def get_game_scores(game_id):

    game = Game.query.get(game_id)

    if not game:

        return error_response(

            "Game not found.",

            404
        )

    scores = GameScore.query.filter_by(

        game_id=game_id

    ).all()

    return success_response(

        [score.to_dict() for score in scores],

        "Scores fetched successfully."
    )


"""
------------------------------------------------------------------------------
CREATE GAME SCORE
------------------------------------------------------------------------------
"""

@game_score_bp.route(

    "/api/games/<int:game_id>/scores",

    methods=["POST"]
)
def create_game_score(game_id):

    game = Game.query.get(game_id)

    if not game:

        return error_response(

            "Game not found.",

            404
        )

    data = request_data()

    missing = missing_fields(

        data,

        [
            "team_id",
            "final_score"
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
    VALIDATE TEAM
    --------------------------------------------------------------------------
    """

    team_id, team_error = parse_int(

        data["team_id"],

        "team_id"
    )

    final_score, score_error = parse_float(

        data["final_score"],

        "final_score"
    )

    errors = [

        error

        for error in [

            team_error,
            score_error

        ]

        if error
    ]

    if errors:

        return error_response(

            "Invalid score data.",

            400,

            errors
        )

    team = Team.query.get(team_id)

    if not team:

        return error_response(

            "Team not found.",

            404
        )

    """
    --------------------------------------------------------------------------
    ENSURE TEAM BELONGS TO SAME EVENT
    --------------------------------------------------------------------------
    """

    if (

        team.event_id

        !=

        game.event_sport.event_id
    ):

        return error_response(

            "Team does not belong to this event.",

            400
        )

    """
    --------------------------------------------------------------------------
    CREATE SCORE
    --------------------------------------------------------------------------
    """

    score = GameScore(

        game_id=game_id,

        team_id=team_id,

        final_score=final_score
    )

    db.session.add(score)

    db.session.commit()

    return success_response(

        score.to_dict(),

        "Game score created successfully.",

        201
    )