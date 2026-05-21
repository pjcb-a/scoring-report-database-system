from flask import Blueprint, request

from app.extensions import db

from app.models.sport import Sport
from app.models.event import Event
from app.models.event_sport import EventSport

from app.utils.responses import (

    success_response,

    error_response
)


sport_bp = Blueprint(

    'sport_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| GET SPORTS BY EVENT
|--------------------------------------------------------------------------
|
| Returns all sports linked to a specific event.
|
"""


@sport_bp.route(

    '/events/<int:event_id>/sports',

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
                **event_sport.sport.to_dict(),

                'event_sport_id':
                    event_sport.event_sport_id
            }

            for event_sport in event_sports
        ]

        return success_response(

            data=data,

            message='Sports fetched successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to fetch sports.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| CREATE SPORT FOR EVENT
|--------------------------------------------------------------------------
|
| Creates a sport and links it to an event.
|
"""


@sport_bp.route(

    '/events/<int:event_id>/sports',

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

        sport_name = payload.get(
            'sport_name'
        )

        scoring_type_id = payload.get(
            'scoring_type_id'
        )

        """
        ----------------------------------------------------------------------
        VALIDATION
        ----------------------------------------------------------------------
        """

        validation_errors = {}

        if not sport_name:

            validation_errors[
                'sport_name'
            ] = [

                'Sport name is required.'
            ]

        if not scoring_type_id:

            validation_errors[
                'scoring_type_id'
            ] = [

                'Scoring type is required.'
            ]

        if validation_errors:

            return error_response(

                message='Validation failed.',

                errors=validation_errors,

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        CREATE SPORT
        ----------------------------------------------------------------------
        """

        sport = Sport(

            sport_name=sport_name,

            scoring_type_id=scoring_type_id
        )

        db.session.add(sport)

        db.session.flush()

        """
        ----------------------------------------------------------------------
        LINK SPORT TO EVENT
        ----------------------------------------------------------------------
        """

        event_sport = EventSport(

            event_id=event_id,

            sport_id=sport.sport_id,

            status="Upcoming"
        )

        db.session.add(event_sport)

        db.session.commit()

        return success_response(

            data={

                **sport.to_dict(),

                'event_sport_id':
                    event_sport.event_sport_id
            },

            message='Sport created successfully.',

            status_code=201
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to create sport.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| UPDATE SPORT
|--------------------------------------------------------------------------
|
| Updates an existing sport.
|
"""


@sport_bp.route(

    '/sports/<int:sport_id>',

    methods=['PUT']
)
def update_sport(sport_id):

    try:

        sport = Sport.query.get(sport_id)

        if not sport:

            return error_response(

                message='Sport not found.',

                status_code=404
            )

        payload = request.get_json()

        if not payload:

            return error_response(

                message='Request body is required.',

                status_code=400
            )

        sport.sport_name = payload.get(

            'sport_name',

            sport.sport_name
        )

        sport.scoring_type_id = payload.get(

            'scoring_type_id',

            sport.scoring_type_id
        )

        db.session.commit()

        return success_response(

            data=sport.to_dict(),

            message='Sport updated successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to update sport.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| DELETE SPORT
|--------------------------------------------------------------------------
|
| Deletes sport-event relationship and sport.
|
"""


@sport_bp.route(

    '/sports/<int:sport_id>',

    methods=['DELETE']
)
def delete_sport(sport_id):

    try:

        sport = Sport.query.get(sport_id)

        if not sport:

            return error_response(

                message='Sport not found.',

                status_code=404
            )

        EventSport.query.filter_by(

            sport_id=sport_id

        ).delete()

        db.session.delete(sport)

        db.session.commit()

        return success_response(

            message='Sport deleted successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to delete sport.',

            errors=[str(e)],

            status_code=500
        )