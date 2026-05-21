from flask import Blueprint, request

from app.extensions import db

from app.models.criteria import Criteria
from app.models.score_component import ScoreComponent

from app.utils.responses import (

    success_response,

    error_response
)


score_component_bp = Blueprint(

    'score_component_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| GET SCORE COMPONENTS
|--------------------------------------------------------------------------
|
| Returns all score components for a criteria.
|
"""


@score_component_bp.route(

    '/criteria/<int:criteria_id>/score-components',

    methods=['GET']
)
def get_score_components(criteria_id):

    try:

        criteria = Criteria.query.get(criteria_id)

        if not criteria:

            return error_response(

                message='Criteria not found.',

                status_code=404
            )

        components = ScoreComponent.query.filter_by(

            criteria_id=criteria_id

        ).all()

        data = [

            component.to_dict()

            for component in components
        ]

        return success_response(

            data=data,

            message='Score components fetched successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to fetch score components.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| CREATE SCORE COMPONENT
|--------------------------------------------------------------------------
|
| Creates a scoring component under a criteria.
|
"""


@score_component_bp.route(

    '/criteria/<int:criteria_id>/score-components',

    methods=['POST']
)
def create_score_component(criteria_id):

    try:

        criteria = Criteria.query.get(criteria_id)

        if not criteria:

            return error_response(

                message='Criteria not found.',

                status_code=404
            )

        payload = request.get_json()

        if not payload:

            return error_response(

                message='Request body is required.',

                status_code=400
            )

        component_name = payload.get(
            'component_name'
        )

        percentage = payload.get(
            'percentage'
        )

        validation_errors = {}

        if not component_name:

            validation_errors[
                'component_name'
            ] = [

                'Component name is required.'
            ]

        if percentage is None:

            validation_errors[
                'percentage'
            ] = [

                'Percentage is required.'
            ]

        if validation_errors:

            return error_response(

                message='Validation failed.',

                errors=validation_errors,

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        VALIDATE TOTAL PERCENTAGE
        ----------------------------------------------------------------------
        """

        existing_total = db.session.query(

            db.func.coalesce(

                db.func.sum(
                    ScoreComponent.percentage
                ),

                0
            )

        ).filter_by(

            criteria_id=criteria_id

        ).scalar()

        new_total = existing_total + float(percentage)

        if new_total > 100:

            return error_response(

                message='Total percentage exceeds 100%.',

                status_code=400
            )

        component = ScoreComponent(

            component_name=component_name,

            percentage=percentage,

            criteria_id=criteria_id
        )

        db.session.add(component)

        db.session.commit()

        return success_response(

            data=component.to_dict(),

            message='Score component created successfully.',

            status_code=201
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to create score component.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| UPDATE SCORE COMPONENT
|--------------------------------------------------------------------------
"""


@score_component_bp.route(

    '/score-components/<int:component_id>',

    methods=['PUT']
)
def update_score_component(component_id):

    try:

        component = ScoreComponent.query.get(

            component_id
        )

        if not component:

            return error_response(

                message='Score component not found.',

                status_code=404
            )

        payload = request.get_json()

        component.component_name = payload.get(

            'component_name',

            component.component_name
        )

        component.percentage = payload.get(

            'percentage',

            component.percentage
        )

        db.session.commit()

        return success_response(

            data=component.to_dict(),

            message='Score component updated successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to update score component.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| DELETE SCORE COMPONENT
|--------------------------------------------------------------------------
"""


@score_component_bp.route(

    '/score-components/<int:component_id>',

    methods=['DELETE']
)
def delete_score_component(component_id):

    try:

        component = ScoreComponent.query.get(

            component_id
        )

        if not component:

            return error_response(

                message='Score component not found.',

                status_code=404
            )

        db.session.delete(component)

        db.session.commit()

        return success_response(

            message='Score component deleted successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to delete score component.',

            errors=[str(e)],

            status_code=500
        )