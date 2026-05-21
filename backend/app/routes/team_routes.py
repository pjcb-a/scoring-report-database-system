from flask import Blueprint, request

from app.extensions import db

from app.models.team import Team
from app.models.event import Event

from app.utils.responses import (

    success_response,

    error_response
)


team_bp = Blueprint(

    'team_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| GET TEAMS BY EVENT
|--------------------------------------------------------------------------
|
| Returns all teams belonging to an event.
|
"""


@team_bp.route(

    '/events/<int:event_id>/teams',

    methods=['GET']
)
def get_event_teams(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        teams = Team.query.filter_by(

            event_id=event_id

        ).all()

        data = [

            team.to_dict()

            for team in teams
        ]

        return success_response(

            data=data,

            message='Teams fetched successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to fetch teams.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| CREATE TEAM
|--------------------------------------------------------------------------
|
| Creates a team under an event.
|
"""


@team_bp.route(

    '/events/<int:event_id>/teams',

    methods=['POST']
)
def create_team(event_id):

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

        team_name = payload.get(
            'team_name'
        )

        team_color = payload.get(
            'team_color'
        )

        """
        ----------------------------------------------------------------------
        VALIDATION
        ----------------------------------------------------------------------
        """

        validation_errors = {}

        if not team_name:

            validation_errors[
                'team_name'
            ] = [

                'Team name is required.'
            ]

        if validation_errors:

            return error_response(

                message='Validation failed.',

                errors=validation_errors,

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        CREATE TEAM
        ----------------------------------------------------------------------
        """

        team = Team(

            team_name=team_name,

            team_color=team_color,

            event_id=event_id
        )

        db.session.add(team)

        db.session.commit()

        return success_response(

            data=team.to_dict(),

            message='Team created successfully.',

            status_code=201
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to create team.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| UPDATE TEAM
|--------------------------------------------------------------------------
|
| Updates a team.
|
"""


@team_bp.route(

    '/teams/<int:team_id>',

    methods=['PUT']
)
def update_team(team_id):

    try:

        team = Team.query.get(team_id)

        if not team:

            return error_response(

                message='Team not found.',

                status_code=404
            )

        payload = request.get_json()

        if not payload:

            return error_response(

                message='Request body is required.',

                status_code=400
            )

        team.team_name = payload.get(

            'team_name',

            team.team_name
        )

        team.team_color = payload.get(

            'team_color',

            team.team_color
        )

        db.session.commit()

        return success_response(

            data=team.to_dict(),

            message='Team updated successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to update team.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| DELETE TEAM
|--------------------------------------------------------------------------
|
| Deletes a team.
|
"""


@team_bp.route(

    '/teams/<int:team_id>',

    methods=['DELETE']
)
def delete_team(team_id):

    try:

        team = Team.query.get(team_id)

        if not team:

            return error_response(

                message='Team not found.',

                status_code=404
            )

        db.session.delete(team)

        db.session.commit()

        return success_response(

            message='Team deleted successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to delete team.',

            errors=[str(e)],

            status_code=500
        )