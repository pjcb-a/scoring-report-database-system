from flask import Blueprint, request

from app.extensions import db

from app.models.criteria import Criteria
from app.models.event import Event
from app.models.event_sport import EventSport

from app.utils.responses import (

    success_response,

    error_response
)


criteria_bp = Blueprint(

    'criteria_bp',

    __name__
)


def _criteria_total_for_event_sport(event_sport_id, exclude_criteria_id=None):
    query = Criteria.query.filter_by(
        event_sport_id=event_sport_id
    )

    if exclude_criteria_id is not None:
        query = query.filter(
            Criteria.criteria_id != exclude_criteria_id
        )

    existing = query.all()

    return sum(
        float(criterion.percentage)
        for criterion in existing
    )


"""
|--------------------------------------------------------------------------
| GET CRITERIA BY EVENT
|--------------------------------------------------------------------------
"""


@criteria_bp.route(
    '/events/<int:event_id>/criteria',
    methods=['GET']
)
def get_event_criteria(event_id):
    try:
        event = Event.query.get(event_id)

        if not event:
            return error_response(
                message='Event not found.',
                status_code=404
            )

        criteria = (
            Criteria.query
            .join(EventSport, Criteria.event_sport_id == EventSport.event_sport_id)
            .filter(EventSport.event_id == event_id)
            .all()
        )

        data = [criterion.to_dict() for criterion in criteria]

        return success_response(
            data=data,
            message='Criteria fetched successfully.'
        )

    except Exception as e:
        return error_response(
            message='Failed to fetch criteria.',
            errors=[str(e)],
            status_code=500
        )


"""
|--------------------------------------------------------------------------
| GET CRITERIA BY EVENT SPORT
|--------------------------------------------------------------------------
"""


@criteria_bp.route(

    '/event-sports/<int:event_sport_id>/criteria',

    methods=['GET']
)
def get_event_sport_criteria(event_sport_id):

    try:

        event_sport = EventSport.query.get(

            event_sport_id
        )

        if not event_sport:

            return error_response(

                message='Event sport not found.',

                status_code=404
            )

        criteria = Criteria.query.filter_by(

            event_sport_id=event_sport_id

        ).all()

        data = [

            criterion.to_dict()

            for criterion in criteria
        ]

        return success_response(

            data=data,

            message='Criteria fetched successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to fetch criteria.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| CREATE CRITERIA
|--------------------------------------------------------------------------
"""


@criteria_bp.route(

    '/event-sports/<int:event_sport_id>/criteria',

    methods=['POST']
)
def create_criteria(event_sport_id):

    try:

        event_sport = EventSport.query.get(

            event_sport_id
        )

        if not event_sport:

            return error_response(

                message='Event sport not found.',

                status_code=404
            )

        payload = request.get_json()

        criteria_name = payload.get(
            'criteria_name'
        )

        percentage = payload.get(
            'percentage'
        )

        validation_errors = {}

        if not criteria_name:

            validation_errors[
                'criteria_name'
            ] = [

                'Criteria name is required.'
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

        try:

            percentage_value = float(percentage)

        except (TypeError, ValueError):

            return error_response(

                message='Validation failed.',

                errors={
                    'percentage': ['Percentage must be a valid number.']
                },

                status_code=400
            )

        if percentage_value <= 0:

            return error_response(

                message='Validation failed.',

                errors={
                    'percentage': ['Percentage must be greater than 0.']
                },

                status_code=400
            )

        existing_total = _criteria_total_for_event_sport(
            event_sport_id
        )

        if existing_total + percentage_value > 100:

            return error_response(

                message='Validation failed.',

                errors={
                    'percentage': [
                        f'Total criteria percentage cannot exceed 100%. '
                        f'Only {100 - existing_total:g}% remaining.'
                    ]
                },

                status_code=400
            )

        criterion = Criteria(

            criteria_name=criteria_name,

            percentage=percentage_value,

            event_sport_id=event_sport_id
        )

        db.session.add(criterion)

        db.session.commit()

        return success_response(

            data=criterion.to_dict(),

            message='Criteria created successfully.',

            status_code=201
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to create criteria.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| UPDATE CRITERIA
|--------------------------------------------------------------------------
"""


@criteria_bp.route(

    '/criteria/<int:criteria_id>',

    methods=['PUT']
)
def update_criteria(criteria_id):

    try:

        criterion = Criteria.query.get(

            criteria_id
        )

        if not criterion:

            return error_response(

                message='Criteria not found.',

                status_code=404
            )

        payload = request.get_json() or {}

        if 'criteria_name' in payload:

            criterion.criteria_name = payload.get(
                'criteria_name',
                criterion.criteria_name
            )

        if 'percentage' in payload:

            try:

                percentage_value = float(
                    payload.get('percentage')
                )

            except (TypeError, ValueError):

                return error_response(

                    message='Validation failed.',

                    errors={
                        'percentage': ['Percentage must be a valid number.']
                    },

                    status_code=400
                )

            if percentage_value <= 0:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'percentage': ['Percentage must be greater than 0.']
                    },

                    status_code=400
                )

            existing_total = _criteria_total_for_event_sport(
                criterion.event_sport_id,
                exclude_criteria_id=criteria_id
            )

            if existing_total + percentage_value > 100:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'percentage': [
                            f'Total criteria percentage cannot exceed 100%. '
                            f'Only {100 - existing_total:g}% remaining.'
                        ]
                    },

                    status_code=400
                )

            criterion.percentage = percentage_value

        db.session.commit()

        return success_response(

            data=criterion.to_dict(),

            message='Criteria updated successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to update criteria.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| DELETE CRITERIA
|--------------------------------------------------------------------------
"""


@criteria_bp.route(

    '/criteria/<int:criteria_id>',

    methods=['DELETE']
)
def delete_criteria(criteria_id):

    try:

        criterion = Criteria.query.get(

            criteria_id
        )

        if not criterion:

            return error_response(

                message='Criteria not found.',

                status_code=404
            )

        db.session.delete(criterion)

        db.session.commit()

        return success_response(

            message='Criteria deleted successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to delete criteria.',

            errors=[str(e)],

            status_code=500
        )