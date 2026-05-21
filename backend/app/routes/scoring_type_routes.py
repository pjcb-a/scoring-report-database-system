from flask import Blueprint, request

from app.extensions import db

from app.models.scoring_type import ScoringType

from app.utils.responses import (

    success_response,

    error_response
)


scoring_type_bp = Blueprint(

    'scoring_type_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| GET SCORING TYPES
|--------------------------------------------------------------------------
|
| Returns all scoring types.
|
"""


@scoring_type_bp.route(

    '/scoring-types',

    methods=['GET']
)
def get_scoring_types():

    try:

        scoring_types = ScoringType.query.all()

        data = [

            scoring_type.to_dict()

            for scoring_type in scoring_types
        ]

        return success_response(

            data=data,

            message='Scoring types fetched successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to fetch scoring types.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| CREATE SCORING TYPE
|--------------------------------------------------------------------------
"""


@scoring_type_bp.route(

    '/scoring-types',

    methods=['POST']
)
def create_scoring_type():

    try:

        payload = request.get_json()

        if not payload:

            return error_response(

                message='Request body is required.',

                status_code=400
            )

        scoring_name = payload.get(
            'scoring_name'
        )

        validation_errors = {}

        if not scoring_name:

            validation_errors[
                'scoring_name'
            ] = [

                'Scoring type name is required.'
            ]

        if validation_errors:

            return error_response(

                message='Validation failed.',

                errors=validation_errors,

                status_code=400
            )

        existing_type = ScoringType.query.filter_by(

            scoring_name=scoring_name

        ).first()

        if existing_type:

            return error_response(

                message='Scoring type already exists.',

                status_code=400
            )

        scoring_type = ScoringType(

            scoring_name=scoring_name
        )

        db.session.add(scoring_type)

        db.session.commit()

        return success_response(

            data=scoring_type.to_dict(),

            message='Scoring type created successfully.',

            status_code=201
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to create scoring type.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| DELETE SCORING TYPE
|--------------------------------------------------------------------------
"""


@scoring_type_bp.route(

    '/scoring-types/<int:scoring_type_id>',

    methods=['DELETE']
)
def delete_scoring_type(scoring_type_id):

    try:

        scoring_type = ScoringType.query.get(

            scoring_type_id
        )

        if not scoring_type:

            return error_response(

                message='Scoring type not found.',

                status_code=404
            )

        db.session.delete(scoring_type)

        db.session.commit()

        return success_response(

            message='Scoring type deleted successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to delete scoring type.',

            errors=[str(e)],

            status_code=500
        )