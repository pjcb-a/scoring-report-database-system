from flask import Blueprint, request

from app.extensions import db

from app.models.event import Event
from app.models.sport import Sport
from app.models.event_sport import EventSport

from app.utils.responses import (

    success_response,

    error_response
)


event_sport_bp = Blueprint(

    'event_sport_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| GET EVENT SPORTS
|--------------------------------------------------------------------------
|
| Returns all event-sport relationships.
|
"""


@event_sport_bp.route(

    '/events/<int:event_id>/event-sports',

    methods=['GET']
)
def get_event_sports(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        event_sports = EventSport.query.filter_by(

            event_id=event_id

        ).all()

        data = [

            {

                'event_sport_id':
                    event_sport.event_sport_id,

                'event_id':
                    event_sport.event_id,

                'sport':
                    event_sport.sport.to_dict()
            }

            for event_sport in event_sports
        ]

        return success_response(

            data=data,

            message='Event sports fetched successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to fetch event sports.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| CREATE EVENT SPORT
|--------------------------------------------------------------------------
|
| Links a sport to an event.
|
"""


@event_sport_bp.route(

    '/events/<int:event_id>/event-sports',

    methods=['POST']
)
def create_event_sport(event_id):

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

        sport_id = payload.get(
            'sport_id'
        )

        validation_errors = {}

        if not sport_id:

            validation_errors[
                'sport_id'
            ] = [

                'Sport is required.'
            ]

        if validation_errors:

            return error_response(

                message='Validation failed.',

                errors=validation_errors,

                status_code=400
            )

        sport = Sport.query.get(sport_id)

        if not sport:

            return error_response(

                message='Sport not found.',

                status_code=404
            )

        """
        ----------------------------------------------------------------------
        PREVENT DUPLICATE LINK
        ----------------------------------------------------------------------
        """

        existing_link = EventSport.query.filter_by(

            event_id=event_id,

            sport_id=sport_id

        ).first()

        if existing_link:

            return error_response(

                message='Sport already linked to this event.',

                status_code=400
            )

        event_sport = EventSport(

            event_id=event_id,

            sport_id=sport_id,

            status="Upcoming"
        )

        db.session.add(event_sport)

        db.session.commit()

        return success_response(

            data={

                'event_sport_id':
                    event_sport.event_sport_id,

                'event_id':
                    event_sport.event_id,

                'sport':
                    sport.to_dict()
            },

            message='Sport linked successfully.',

            status_code=201
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to link sport.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| DELETE EVENT SPORT
|--------------------------------------------------------------------------
|
| Removes sport from an event.
|
"""


@event_sport_bp.route(

    '/event-sports/<int:event_sport_id>',

    methods=['DELETE']
)
def delete_event_sport(event_sport_id):

    try:

        event_sport = EventSport.query.get(

            event_sport_id
        )

        if not event_sport:

            return error_response(

                message='Event sport not found.',

                status_code=404
            )

        db.session.delete(event_sport)

        db.session.commit()

        return success_response(

            message='Event sport removed successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to remove event sport.',

            errors=[str(e)],

            status_code=500
        )