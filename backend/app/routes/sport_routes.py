from flask import Blueprint, jsonify

from app.models.sport import Sport


sport_bp = Blueprint("sport_bp", __name__)


@sport_bp.route("/api/sports", methods=["GET"])
def get_sports():

    sports = Sport.query.all()

    result = []

    for sport in sports:
        result.append({
            "sport_id": sport.sport_id,
            "sport_name": sport.sport_name,
            "scoring_type": sport.scoring_type.type
        })

    return jsonify(result)