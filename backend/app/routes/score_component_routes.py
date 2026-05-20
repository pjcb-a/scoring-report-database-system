from flask import Blueprint

from app.extensions import db
from app.models.criteria import Criteria
from app.models.game_score import GameScore
from app.models.judge import Judge
from app.models.score_component import ScoreComponent
from app.routes.utils import (
    error_response,
    missing_fields,
    parse_float,
    parse_int,
    request_data,
    success_response
)


score_component_bp = Blueprint("score_component_bp", __name__)


@score_component_bp.route("/api/score-components", methods=["GET"])
def get_score_components():
    components = ScoreComponent.query.order_by(
        ScoreComponent.score_component_id.desc()
    ).all()

    return success_response(
        [component.to_dict() for component in components],
        "Score components fetched successfully."
    )


@score_component_bp.route(
    "/api/score-components/<int:score_component_id>",
    methods=["GET"]
)
def get_score_component(score_component_id):
    component = ScoreComponent.query.get(score_component_id)

    if not component:
        return error_response("Score component not found.", 404)

    return success_response(
        component.to_dict(),
        "Score component fetched successfully."
    )


@score_component_bp.route("/api/score-components", methods=["POST"])
def create_score_component():
    data = request_data()
    missing = missing_fields(
        data,
        ["game_score_id", "criteria_id", "judge_id", "score_value"]
    )

    if missing:
        return error_response("Required fields are missing.", 400, missing)

    game_score_id, game_score_error = parse_int(
        data["game_score_id"],
        "game_score_id"
    )
    criteria_id, criteria_error = parse_int(
        data["criteria_id"],
        "criteria_id"
    )
    judge_id, judge_error = parse_int(data["judge_id"], "judge_id")
    score_value, score_error = parse_float(
        data["score_value"],
        "score_value"
    )
    errors = [
        error
        for error in [
            game_score_error,
            criteria_error,
            judge_error,
            score_error
        ]
        if error
    ]

    if errors:
        return error_response("Invalid score component data.", 400, errors)

    if score_value < 0:
        return error_response("score_value cannot be negative.", 400)

    game_score = GameScore.query.get(game_score_id)
    criteria = Criteria.query.get(criteria_id)

    if not game_score:
        return error_response("Game score not found.", 404)

    if not criteria:
        return error_response("Criteria not found.", 404)

    if not Judge.query.get(judge_id):
        return error_response("Judge not found.", 404)

    game_sport_id = game_score.game.event_sport.sport_id

    if criteria.sport_id != game_sport_id:
        return error_response(
            "Criteria must belong to the scored game's sport.",
            400
        )

    existing = ScoreComponent.query.filter_by(
        game_score_id=game_score_id,
        criteria_id=criteria_id,
        judge_id=judge_id
    ).first()

    if existing:
        return error_response(
            "This judge already scored this criteria for this game score.",
            409
        )

    component = ScoreComponent(
        game_score_id=game_score_id,
        criteria_id=criteria_id,
        judge_id=judge_id,
        score_value=score_value
    )

    db.session.add(component)
    db.session.commit()

    return success_response(
        component.to_dict(),
        "Score component created successfully.",
        201
    )


@score_component_bp.route(
    "/api/score-components/<int:score_component_id>",
    methods=["PUT"]
)
def update_score_component(score_component_id):
    component = ScoreComponent.query.get(score_component_id)

    if not component:
        return error_response("Score component not found.", 404)

    data = request_data()
    game_score_id = component.game_score_id
    criteria_id = component.criteria_id
    judge_id = component.judge_id

    if "game_score_id" in data:
        game_score_id, error = parse_int(
            data["game_score_id"],
            "game_score_id"
        )

        if error:
            return error_response(
                "Invalid score component data.",
                400,
                [error]
            )

        if not GameScore.query.get(game_score_id):
            return error_response("Game score not found.", 404)

    if "criteria_id" in data:
        criteria_id, error = parse_int(data["criteria_id"], "criteria_id")

        if error:
            return error_response(
                "Invalid score component data.",
                400,
                [error]
            )

        if not Criteria.query.get(criteria_id):
            return error_response("Criteria not found.", 404)

    if "judge_id" in data:
        judge_id, error = parse_int(data["judge_id"], "judge_id")

        if error:
            return error_response(
                "Invalid score component data.",
                400,
                [error]
            )

        if not Judge.query.get(judge_id):
            return error_response("Judge not found.", 404)

    duplicate = ScoreComponent.query.filter(
        ScoreComponent.game_score_id == game_score_id,
        ScoreComponent.criteria_id == criteria_id,
        ScoreComponent.judge_id == judge_id,
        ScoreComponent.score_component_id != score_component_id
    ).first()

    if duplicate:
        return error_response(
            "This judge already scored this criteria for this game score.",
            409
        )

    if "score_value" in data:
        score_value, error = parse_float(data["score_value"], "score_value")

        if error:
            return error_response(
                "Invalid score component data.",
                400,
                [error]
            )

        if score_value < 0:
            return error_response("score_value cannot be negative.", 400)

        component.score_value = score_value

    game_score = GameScore.query.get(game_score_id)
    criteria = Criteria.query.get(criteria_id)

    if criteria.sport_id != game_score.game.event_sport.sport_id:
        return error_response(
            "Criteria must belong to the scored game's sport.",
            400
        )

    component.game_score_id = game_score_id
    component.criteria_id = criteria_id
    component.judge_id = judge_id

    db.session.commit()

    return success_response(
        component.to_dict(),
        "Score component updated successfully."
    )


@score_component_bp.route(
    "/api/score-components/<int:score_component_id>",
    methods=["DELETE"]
)
def delete_score_component(score_component_id):
    component = ScoreComponent.query.get(score_component_id)

    if not component:
        return error_response("Score component not found.", 404)

    db.session.delete(component)
    db.session.commit()

    return success_response(
        {"score_component_id": score_component_id},
        "Score component deleted successfully."
    )
