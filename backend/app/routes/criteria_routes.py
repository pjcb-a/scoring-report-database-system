from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.criteria import Criteria


criteria_bp = Blueprint("criteria_bp", __name__)


@criteria_bp.route("/api/criteria", methods=["GET"])
def get_criteria():

    criteria = Criteria.query.all()

    result = []

    for item in criteria:
        result.append({
            "criteria_id": item.criteria_id,
            "criteria_name": item.criteria_name,
            "percentage_weight": item.percentage_weight,
            "sport": item.sport.sport_name
        })

    return jsonify(result)


@criteria_bp.route("/api/criteria", methods=["POST"])
def create_criteria():

    data = request.get_json()

    criteria = Criteria(
        sport_id=data["sport_id"],
        criteria_name=data["criteria_name"],
        percentage_weight=data["percentage_weight"]
    )

    db.session.add(criteria)
    db.session.commit()

    return jsonify({
        "message": "Criteria created successfully"
    }), 201