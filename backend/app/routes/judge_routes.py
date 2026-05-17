from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.judge import Judge


judge_bp = Blueprint("judge_bp", __name__)


@judge_bp.route("/api/judges", methods=["GET"])
def get_judges():

    judges = Judge.query.all()

    result = []

    for judge in judges:
        result.append({
            "judge_id": judge.judge_id,
            "raw_score": judge.raw_score
        })

    return jsonify(result)


@judge_bp.route("/api/judges", methods=["POST"])
def create_judge():

    data = request.get_json()

    judge = Judge(
        judge_name=data["judge_name"],
        raw_score=data["raw_score"]
    )

    db.session.add(judge)
    db.session.commit()

    return jsonify({
        "message": "Judge created successfully"
    }), 201