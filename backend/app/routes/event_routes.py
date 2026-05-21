from flask import Blueprint, request

from app.extensions import db

from app.models.event import Event

from app.utils.responses import (

    success_response,

    error_response
)


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

    '/',

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

    except Exception as e:

        return error_response(

            message='Failed to fetch events.',

            errors=[str(e)],

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

    '/<int:event_id>',

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

    except Exception as e:

        return error_response(

            message='Failed to fetch event.',

            errors=[str(e)],

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

    '/',

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

            start_day=start_day,

            end_day=end_day,

            status=status
        )

        db.session.add(new_event)

        db.session.commit()

        return success_response(

            data=new_event.to_dict(),

            message='Event created successfully.',

            status_code=201
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to create event.',

            errors=[str(e)],

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

    '/<int:event_id>',

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

        """
        ----------------------------------------------------------------------
        UPDATE FIELDS
        ----------------------------------------------------------------------
        """

        event.event_name = payload.get(

            'event_name',

            event.event_name
        )

        event.start_day = payload.get(

            'start_day',

            event.start_day
        )

        event.end_day = payload.get(

            'end_day',

            event.end_day
        )

        event.status = payload.get(

            'status',

            event.status
        )

        db.session.commit()

        return success_response(

            data=event.to_dict(),

            message='Event updated successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to update event.',

            errors=[str(e)],

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

    '/<int:event_id>',

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

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to delete event.',

            errors=[str(e)],

            status_code=500
        )