from sqlalchemy import func

from flask import Blueprint

from app.extensions import db
from app.models.scoring_type import ScoringType
from app.models.sport import Sport
from app.routes.utils import (
    clean_string,
    error_response,
    missing_fields,
    parse_int,
    request_data,
    success_response
)


sport_bp = Blueprint("sport_bp", __name__)


@sport_bp.route("/api/sports", methods=["GET"])
def get_sports():
    sports = Sport.query.order_by(Sport.sport_name.asc()).all()

    return success_response(
        [sport.to_dict() for sport in sports],
        "Sports fetched successfully."
    )


@sport_bp.route("/api/sports/<int:sport_id>", methods=["GET"])
def get_sport(sport_id):
    sport = Sport.query.get(sport_id)

    if not sport:
        return error_response("Sport not found.", 404)

    return success_response(
        sport.to_dict(),
        "Sport fetched successfully."
    )


@sport_bp.route("/api/sports", methods=["POST"])
def create_sport():
    data = request_data()
    missing = missing_fields(data, ["sport_name", "scoring_type_id"])

    if missing:
        return error_response("Required fields are missing.", 400, missing)

    sport_name = clean_string(data["sport_name"])
    scoring_type_id, error = parse_int(
        data["scoring_type_id"],
        "scoring_type_id"
    )

    if error:
        return error_response("Invalid sport data.", 400, [error])

    scoring_type = ScoringType.query.get(scoring_type_id)

    if not scoring_type:
        return error_response("Scoring type not found.", 404)

    existing = Sport.query.filter(
        func.lower(Sport.sport_name) == sport_name.lower()
    ).first()

    if existing:
        return error_response("Sport name already exists.", 409)

    sport = Sport(
        sport_name=sport_name,
        scoring_type_id=scoring_type_id
    )

    db.session.add(sport)
    db.session.commit()

    return success_response(
        sport.to_dict(),
        "Sport created successfully.",
        201
    )


@sport_bp.route("/api/sports/<int:sport_id>", methods=["PUT"])
def update_sport(sport_id):
    sport = Sport.query.get(sport_id)

    if not sport:
        return error_response("Sport not found.", 404)

    data = request_data()

    if "sport_name" in data:
        sport_name = clean_string(data["sport_name"])

        if not sport_name:
            return error_response("sport_name is required.", 400)

        existing = Sport.query.filter(
            func.lower(Sport.sport_name) == sport_name.lower(),
            Sport.sport_id != sport_id
        ).first()

        if existing:
            return error_response("Sport name already exists.", 409)

        sport.sport_name = sport_name

    if "scoring_type_id" in data:
        scoring_type_id, error = parse_int(
            data["scoring_type_id"],
            "scoring_type_id"
        )

        if error:
            return error_response("Invalid sport data.", 400, [error])

        scoring_type = ScoringType.query.get(scoring_type_id)

        if not scoring_type:
            return error_response("Scoring type not found.", 404)

        sport.scoring_type_id = scoring_type_id

    db.session.commit()

    return success_response(
        sport.to_dict(),
        "Sport updated successfully."
    )


@sport_bp.route("/api/sports/<int:sport_id>", methods=["DELETE"])
def delete_sport(sport_id):
    sport = Sport.query.get(sport_id)

    if not sport:
        return error_response("Sport not found.", 404)

    db.session.delete(sport)
    db.session.commit()

    return success_response(
        {"sport_id": sport_id},
        "Sport deleted successfully."
    )
