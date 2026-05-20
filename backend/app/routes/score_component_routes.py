from flask import Blueprint

from app.extensions import db

from app.models.criteria import Criteria
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


score_component_bp = Blueprint(

    "score_component_bp",

    __name__
)


"""
------------------------------------------------------------------------------
GET SCORE COMPONENTS OF JUDGE
------------------------------------------------------------------------------
"""

@score_component_bp.route(

    "/api/judges/<int:judge_id>/components",

    methods=["GET"]
)
def get_score_components(judge_id):

    judge = Judge.query.get(judge_id)

    if not judge:

        return error_response(

            "Judge not found.",

            404
        )

    components = ScoreComponent.query.filter_by(

        judge_id=judge_id

    ).all()

    return success_response(

        [
            component.to_dict()
            for component in components
        ],

        "Score components fetched successfully."
    )


"""
------------------------------------------------------------------------------
CREATE SCORE COMPONENT
------------------------------------------------------------------------------
"""

@score_component_bp.route(

    "/api/judges/<int:judge_id>/components",

    methods=["POST"]
)
def create_score_component(judge_id):

    judge = Judge.query.get(judge_id)

    if not judge:

        return error_response(

            "Judge not found.",

            404
        )

    data = request_data()

    missing = missing_fields(

        data,

        [
            "criteria_id",
            "component_score"
        ]
    )

    if missing:

        return error_response(

            "Required fields are missing.",

            400,

            missing
        )

    criteria_id, criteria_error = parse_int(

        data["criteria_id"],

        "criteria_id"
    )

    component_score, score_error = parse_float(

        data["component_score"],

        "component_score"
    )

    errors = [

        error

        for error in [

            criteria_error,
            score_error

        ]

        if error
    ]

    if errors:

        return error_response(

            "Invalid score component data.",

            400,

            errors
        )

    criteria = Criteria.query.get(criteria_id)

    if not criteria:

        return error_response(

            "Criteria not found.",

            404
        )

    component = ScoreComponent(

        judge_id=judge_id,

        criteria_id=criteria_id,

        component_score=component_score
    )

    db.session.add(component)

    db.session.commit()

    return success_response(

        component.to_dict(),

        "Score component created successfully.",

        201
    )