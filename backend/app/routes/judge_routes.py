from flask import Blueprint, request

from app.extensions import db

from app.models.event import Event
from app.models.judge import Judge

from app.utils.responses import (

    success_response,

    error_response
)


judge_bp = Blueprint(

    'judge_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| GET JUDGES BY EVENT
|--------------------------------------------------------------------------
"""


@judge_bp.route(

    '/events/<int:event_id>/judges',

    methods=['GET']
)
def get_event_judges(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        judges = Judge.query.filter_by(

            event_id=event_id

        ).all()

        data = [

            judge.to_dict()

            for judge in judges
        ]

        return success_response(

            data=data,

            message='Judges fetched successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to fetch judges.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| CREATE JUDGE
|--------------------------------------------------------------------------
"""


@judge_bp.route(

    '/events/<int:event_id>/judges',

    methods=['POST']
)
def create_judge(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        payload = request.get_json()

        if not payload:

            return error_response(

                message='Request body is required.',

                status_code=400
            )

        judge_name = payload.get(
            'judge_name'
        )

        validation_errors = {}

        if not judge_name:

            validation_errors[
                'judge_name'
            ] = [

                'Judge name is required.'
            ]

        if validation_errors:

            return error_response(

                message='Validation failed.',

                errors=validation_errors,

                status_code=400
            )

        judge = Judge(

            judge_name=judge_name,

            event_id=event_id
        )

        db.session.add(judge)

        db.session.commit()

        return success_response(

            data=judge.to_dict(),

            message='Judge created successfully.',

            status_code=201
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to create judge.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| UPDATE JUDGE
|--------------------------------------------------------------------------
"""


@judge_bp.route(

    '/judges/<int:judge_id>',

    methods=['PUT']
)
def update_judge(judge_id):

    try:

        judge = Judge.query.get(judge_id)

        if not judge:

            return error_response(

                message='Judge not found.',

                status_code=404
            )

        payload = request.get_json()

        judge.judge_name = payload.get(

            'judge_name',

            judge.judge_name
        )

        db.session.commit()

        return success_response(

            data=judge.to_dict(),

            message='Judge updated successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to update judge.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| DELETE JUDGE
|--------------------------------------------------------------------------
"""


@judge_bp.route(

    '/judges/<int:judge_id>',

    methods=['DELETE']
)
def delete_judge(judge_id):

    try:

        judge = Judge.query.get(judge_id)

        if not judge:

            return error_response(

                message='Judge not found.',

                status_code=404
            )

        db.session.delete(judge)

        db.session.commit()

        return success_response(

            message='Judge deleted successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to delete judge.',

            errors=[str(e)],

            status_code=500
        )