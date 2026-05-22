from datetime import date

from flask import Blueprint, request

from app.extensions import db

from app.models.event import Event

from app.utils.responses import (

    success_response,

    error_response
)

ALLOWED_EVENT_STATUSES = {
    'Upcoming',
    'Ongoing',
    'Completed',
    'Active'
}


def normalize_event_status(status):
    if status == 'Active':
        return 'Ongoing'
    if status in {'Upcoming', 'Ongoing', 'Completed'}:
        return status
    return None


def parse_event_date(value, field_label):
    if value is None or value == '':
        return None, f'{field_label} is required.'

    if isinstance(value, date):
        return value, None

    try:
        return date.fromisoformat(str(value)[:10]), None
    except (TypeError, ValueError):
        return None, f'{field_label} must be a valid date.'


event_bp = Blueprint(

    'event_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| GET ALL EVENTS
|--------------------------------------------------------------------------
|
| Returns all events ordered by latest start date.
|
"""


@event_bp.route(

    '/events',

    methods=['GET']
)
def get_events():

    try:

        events = Event.query.order_by(

            Event.start_day.desc()

        ).all()

        data = [

            event.to_dict()

            for event in events
        ]

        return success_response(

            data=data,

            message='Events fetched successfully.'
        )

    except Exception as error:

        return error_response(

            message='Failed to fetch events.',

            errors=[str(error)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| GET SINGLE EVENT
|--------------------------------------------------------------------------
|
| Returns a single event by ID.
|
"""


@event_bp.route(

    '/events/<int:event_id>',

    methods=['GET']
)
def get_event(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        return success_response(

            data=event.to_dict(),

            message='Event fetched successfully.'
        )

    except Exception as error:

        return error_response(

            message='Failed to fetch event.',

            errors=[str(error)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| CREATE EVENT
|--------------------------------------------------------------------------
|
| Creates a new event.
|
"""


@event_bp.route(

    '/events',

    methods=['POST']
)
def create_event():

    try:

        payload = request.get_json()

        if not payload:

            return error_response(

                message='Request body is required.',

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        PAYLOAD
        ----------------------------------------------------------------------
        """

        event_name = payload.get(

            'event_name'
        )

        start_day = payload.get(

            'start_day'
        )

        end_day = payload.get(

            'end_day'
        )

        status = payload.get(

            'status',

            'Upcoming'
        )

        """
        ----------------------------------------------------------------------
        VALIDATION
        ----------------------------------------------------------------------
        """

        validation_errors = {}

        if not event_name:

            validation_errors[
                'event_name'
            ] = [

                'Event name is required.'
            ]

        if not start_day:

            validation_errors[
                'start_day'
            ] = [

                'Start day is required.'
            ]

        if not end_day:

            validation_errors[
                'end_day'
            ] = [

                'End day is required.'
            ]

        normalized_status = normalize_event_status(status)

        if not normalized_status:

            validation_errors['status'] = [
                'Status must be Upcoming, Ongoing, or Completed.'
            ]

        start_date, start_error = parse_event_date(
            start_day,
            'Start day'
        )

        if start_error:

            validation_errors['start_day'] = [start_error]

        end_date, end_error = parse_event_date(
            end_day,
            'End day'
        )

        if end_error:

            validation_errors['end_day'] = [end_error]

        if (
            start_date
            and end_date
            and end_date < start_date
        ):

            validation_errors['end_day'] = [
                'End day cannot be before start day.'
            ]

        if validation_errors:

            return error_response(

                message='Validation failed.',

                errors=validation_errors,

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        CREATE EVENT
        ----------------------------------------------------------------------
        """

        new_event = Event(

            event_name=event_name,

            start_day=start_date,

            end_day=end_date,

            status=normalized_status
        )

        db.session.add(new_event)

        db.session.commit()

        return success_response(

            data=new_event.to_dict(),

            message='Event created successfully.',

            status_code=201
        )

    except Exception as error:

        db.session.rollback()

        return error_response(

            message='Failed to create event.',

            errors=[str(error)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| UPDATE EVENT
|--------------------------------------------------------------------------
|
| Updates an existing event.
|
"""


@event_bp.route(

    '/events/<int:event_id>',

    methods=['PUT']
)
def update_event(event_id):

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

        validation_errors = {}

        if 'event_name' in payload:

            event_name = payload.get('event_name')

            if not event_name:

                validation_errors['event_name'] = [
                    'Event name is required.'
                ]
            else:

                event.event_name = event_name

        start_day_value = (
            payload.get('start_day')
            if 'start_day' in payload
            else None
        )

        end_day_value = (
            payload.get('end_day')
            if 'end_day' in payload
            else None
        )

        start_date = event.start_day

        end_date = event.end_day

        if start_day_value is not None:

            start_date, start_error = parse_event_date(
                start_day_value,
                'Start day'
            )

            if start_error:

                validation_errors['start_day'] = [start_error]
            else:

                event.start_day = start_date

        if end_day_value is not None:

            end_date, end_error = parse_event_date(
                end_day_value,
                'End day'
            )

            if end_error:

                validation_errors['end_day'] = [end_error]
            else:

                event.end_day = end_date

        if (
            event.start_day
            and event.end_day
            and event.end_day < event.start_day
        ):

            validation_errors['end_day'] = [
                'End day cannot be before start day.'
            ]

        if 'status' in payload:

            normalized_status = normalize_event_status(
                payload.get('status')
            )

            if not normalized_status:

                validation_errors['status'] = [
                    'Status must be Upcoming, Ongoing, or Completed.'
                ]
            else:

                event.status = normalized_status

        if validation_errors:

            return error_response(

                message='Validation failed.',

                errors=validation_errors,

                status_code=400
            )

        db.session.commit()

        return success_response(

            data=event.to_dict(),

            message='Event updated successfully.'
        )

    except Exception as error:

        db.session.rollback()

        return error_response(

            message='Failed to update event.',

            errors=[str(error)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| DELETE EVENT
|--------------------------------------------------------------------------
|
| Deletes an event.
|
"""


@event_bp.route(

    '/events/<int:event_id>',

    methods=['DELETE']
)
def delete_event(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        db.session.delete(event)

        db.session.commit()

        return success_response(

            message='Event deleted successfully.'
        )

    except Exception as error:

        db.session.rollback()

        return error_response(

            message='Failed to delete event.',

            errors=[str(error)],

            status_code=500
        )