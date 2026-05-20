from flask import Blueprint

from app.extensions import db

from app.models.game import Game
from app.models.judge import Judge

from app.routes.utils import (

    error_response,

    missing_fields,

    parse_float,

    parse_int,

    request_data,

    success_response
)


judge_bp = Blueprint(

    "judge_bp",

    __name__
)


"""
------------------------------------------------------------------------------
GET JUDGES OF GAME
------------------------------------------------------------------------------
"""

@judge_bp.route(

    "/api/games/<int:game_id>/judges",

    methods=["GET"]
)
def get_judges_by_game(game_id):

    game = Game.query.get(game_id)

    if not game:

        return error_response(

            "Game not found.",

            404
        )

    judges = Judge.query.filter_by(

        game_id=game_id

    ).all()

    return success_response(

        [judge.to_dict() for judge in judges],

        "Judges fetched successfully."
    )


"""
------------------------------------------------------------------------------
CREATE JUDGE SCORE
------------------------------------------------------------------------------
"""

@judge_bp.route(

    "/api/games/<int:game_id>/judges",

    methods=["POST"]
)
def create_judge(game_id):

    game = Game.query.get(game_id)

    if not game:

        return error_response(

            "Game not found.",

            404
        )

    data = request_data()

    missing = missing_fields(

        data,

        ["raw_score"]
    )

    if missing:

        return error_response(

            "Required fields are missing.",

            400,

            missing
        )

    raw_score, error = parse_float(

        data["raw_score"],

        "raw_score"
    )

    if error:

        return error_response(

            "Invalid judge data.",

            400,

            [error]
        )

    judge = Judge(

        game_id=game_id,

        raw_score=raw_score
    )

    db.session.add(judge)

    db.session.commit()

    return success_response(

        judge.to_dict(),

        "Judge score created successfully.",

        201
    )