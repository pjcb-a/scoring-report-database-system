from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.score_component import ScoreComponent


score_component_bp = Blueprint("score_component_bp", __name__)


@score_component_bp.route("/api/score-components", methods=["GET"])
def get_score_components():

    components = ScoreComponent.query.all()

    result = []

    for component in components:
        result.append({
            "score_component_id": component.score_component_id,
            "judge": component.judge.judge_name,
            "criteria": component.criteria.criteria_name,
            "score_value": component.score_value
        })

    return jsonify(result)


@score_component_bp.route("/api/score-components", methods=["POST"])
def create_score_component():

    data = request.get_json()

    component = ScoreComponent(
        game_score_id=data["game_score_id"],
        criteria_id=data["criteria_id"],
        judge_id=data["judge_id"],
        score_value=data["score_value"]
    )

    db.session.add(component)
    db.session.commit()

    return jsonify({
        "message": "Score component created successfully"
    }), 201