from flask import Blueprint

from app.models.scoring_type import ScoringType
from app.routes.utils import error_response, success_response


scoring_type_bp = Blueprint("scoring_type_bp", __name__)


@scoring_type_bp.route("/api/scoring-types", methods=["GET"])
def get_scoring_types():
    scoring_types = ScoringType.query.order_by(
        ScoringType.scoring_type_id.asc()
    ).all()

    return success_response(
        [scoring_type.to_dict() for scoring_type in scoring_types],
        "Scoring types fetched successfully."
    )


@scoring_type_bp.route(
    "/api/scoring-types/<int:scoring_type_id>",
    methods=["GET"]
)
def get_scoring_type(scoring_type_id):
    scoring_type = ScoringType.query.get(scoring_type_id)

    if not scoring_type:
        return error_response("Scoring type not found.", 404)

    return success_response(
        scoring_type.to_dict(),
        "Scoring type fetched successfully."
    )
