from sqlalchemy import func

from flask import Blueprint

from app.extensions import db
from app.models.criteria import Criteria
from app.models.sport import Sport
from app.routes.utils import (
    clean_string,
    error_response,
    missing_fields,
    parse_float,
    parse_int,
    request_data,
    success_response
)


criteria_bp = Blueprint("criteria_bp", __name__)


@criteria_bp.route("/api/criteria", methods=["GET"])
def get_criteria():
    criteria = Criteria.query.order_by(Criteria.criteria_name.asc()).all()

    return success_response(
        [item.to_dict() for item in criteria],
        "Criteria fetched successfully."
    )


@criteria_bp.route("/api/criteria/<int:criteria_id>", methods=["GET"])
def get_criterion(criteria_id):
    criterion = Criteria.query.get(criteria_id)

    if not criterion:
        return error_response("Criteria not found.", 404)

    return success_response(
        criterion.to_dict(),
        "Criteria fetched successfully."
    )


@criteria_bp.route("/api/criteria", methods=["POST"])
def create_criteria():
    data = request_data()
    missing = missing_fields(
        data,
        ["sport_id", "criteria_name", "percentage_weight"]
    )

    if missing:
        return error_response("Required fields are missing.", 400, missing)

    sport_id, sport_error = parse_int(data["sport_id"], "sport_id")
    percentage_weight, weight_error = parse_float(
        data["percentage_weight"],
        "percentage_weight"
    )
    errors = [error for error in [sport_error, weight_error] if error]

    if errors:
        return error_response("Invalid criteria data.", 400, errors)

    if percentage_weight < 0 or percentage_weight > 100:
        return error_response(
            "percentage_weight must be between 0 and 100.",
            400
        )

    sport = Sport.query.get(sport_id)

    if not sport:
        return error_response("Sport not found.", 404)

    criteria_name = clean_string(data["criteria_name"])
    existing = Criteria.query.filter(
        Criteria.sport_id == sport_id,
        func.lower(Criteria.criteria_name) == criteria_name.lower()
    ).first()

    if existing:
        return error_response(
            "Criteria already exists for this sport.",
            409
        )

    criterion = Criteria(
        sport_id=sport_id,
        criteria_name=criteria_name,
        percentage_weight=percentage_weight
    )

    db.session.add(criterion)
    db.session.commit()

    return success_response(
        criterion.to_dict(),
        "Criteria created successfully.",
        201
    )


@criteria_bp.route("/api/criteria/<int:criteria_id>", methods=["PUT"])
def update_criteria(criteria_id):
    criterion = Criteria.query.get(criteria_id)

    if not criterion:
        return error_response("Criteria not found.", 404)

    data = request_data()
    sport_id = criterion.sport_id

    if "sport_id" in data:
        sport_id, error = parse_int(data["sport_id"], "sport_id")

        if error:
            return error_response("Invalid criteria data.", 400, [error])

        sport = Sport.query.get(sport_id)

        if not sport:
            return error_response("Sport not found.", 404)

        criterion.sport_id = sport_id

    if "criteria_name" in data:
        criteria_name = clean_string(data["criteria_name"])

        if not criteria_name:
            return error_response("criteria_name is required.", 400)

        existing = Criteria.query.filter(
            Criteria.sport_id == sport_id,
            func.lower(Criteria.criteria_name) == criteria_name.lower(),
            Criteria.criteria_id != criteria_id
        ).first()

        if existing:
            return error_response(
                "Criteria already exists for this sport.",
                409
            )

        criterion.criteria_name = criteria_name

    if "percentage_weight" in data:
        percentage_weight, error = parse_float(
            data["percentage_weight"],
            "percentage_weight"
        )

        if error:
            return error_response("Invalid criteria data.", 400, [error])

        if percentage_weight < 0 or percentage_weight > 100:
            return error_response(
                "percentage_weight must be between 0 and 100.",
                400
            )

        criterion.percentage_weight = percentage_weight

    db.session.commit()

    return success_response(
        criterion.to_dict(),
        "Criteria updated successfully."
    )


@criteria_bp.route("/api/criteria/<int:criteria_id>", methods=["DELETE"])
def delete_criteria(criteria_id):
    criterion = Criteria.query.get(criteria_id)

    if not criterion:
        return error_response("Criteria not found.", 404)

    db.session.delete(criterion)
    db.session.commit()

    return success_response(
        {"criteria_id": criteria_id},
        "Criteria deleted successfully."
    )
