from sqlalchemy import func

from flask import Blueprint

from app.extensions import db
from app.models.judge import Judge
from app.routes.utils import (
    clean_string,
    error_response,
    missing_fields,
    request_data,
    success_response
)


judge_bp = Blueprint("judge_bp", __name__)


@judge_bp.route("/api/judges", methods=["GET"])
def get_judges():
    judges = Judge.query.order_by(Judge.judge_name.asc()).all()

    return success_response(
        [judge.to_dict() for judge in judges],
        "Judges fetched successfully."
    )


@judge_bp.route("/api/judges/<int:judge_id>", methods=["GET"])
def get_judge(judge_id):
    judge = Judge.query.get(judge_id)

    if not judge:
        return error_response("Judge not found.", 404)

    return success_response(
        judge.to_dict(),
        "Judge fetched successfully."
    )


@judge_bp.route("/api/judges", methods=["POST"])
def create_judge():
    data = request_data()
    missing = missing_fields(data, ["judge_name"])

    if missing:
        return error_response("Required fields are missing.", 400, missing)

    judge_name = clean_string(data["judge_name"])
    existing = Judge.query.filter(
        func.lower(Judge.judge_name) == judge_name.lower()
    ).first()

    if existing:
        return error_response("Judge name already exists.", 409)

    judge = Judge(judge_name=judge_name)

    db.session.add(judge)
    db.session.commit()

    return success_response(
        judge.to_dict(),
        "Judge created successfully.",
        201
    )


@judge_bp.route("/api/judges/<int:judge_id>", methods=["PUT"])
def update_judge(judge_id):
    judge = Judge.query.get(judge_id)

    if not judge:
        return error_response("Judge not found.", 404)

    data = request_data()

    if "judge_name" in data:
        judge_name = clean_string(data["judge_name"])

        if not judge_name:
            return error_response("judge_name is required.", 400)

        existing = Judge.query.filter(
            func.lower(Judge.judge_name) == judge_name.lower(),
            Judge.judge_id != judge_id
        ).first()

        if existing:
            return error_response("Judge name already exists.", 409)

        judge.judge_name = judge_name

    db.session.commit()

    return success_response(
        judge.to_dict(),
        "Judge updated successfully."
    )


@judge_bp.route("/api/judges/<int:judge_id>", methods=["DELETE"])
def delete_judge(judge_id):
    judge = Judge.query.get(judge_id)

    if not judge:
        return error_response("Judge not found.", 404)

    db.session.delete(judge)
    db.session.commit()

    return success_response(
        {"judge_id": judge_id},
        "Judge deleted successfully."
    )
