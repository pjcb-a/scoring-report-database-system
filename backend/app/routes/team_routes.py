from sqlalchemy import func

from flask import Blueprint

from app.extensions import db
from app.models.team import Team
from app.routes.utils import (
    clean_string,
    error_response,
    missing_fields,
    request_data,
    success_response
)


team_bp = Blueprint("team_bp", __name__)


@team_bp.route("/api/teams", methods=["GET"])
def get_teams():
    teams = Team.query.order_by(Team.team_name.asc()).all()

    return success_response(
        [team.to_dict() for team in teams],
        "Teams fetched successfully."
    )


@team_bp.route("/api/teams/<int:team_id>", methods=["GET"])
def get_team(team_id):
    team = Team.query.get(team_id)

    if not team:
        return error_response("Team not found.", 404)

    return success_response(
        team.to_dict(),
        "Team fetched successfully."
    )


@team_bp.route("/api/teams", methods=["POST"])
def create_team():
    data = request_data()
    missing = missing_fields(data, ["team_name", "team_color"])

    if missing:
        return error_response("Required fields are missing.", 400, missing)

    team_name = clean_string(data["team_name"])
    team_color = clean_string(data["team_color"])

    existing = Team.query.filter(
        func.lower(Team.team_name) == team_name.lower()
    ).first()

    if existing:
        return error_response("Team name already exists.", 409)

    team = Team(team_name=team_name, team_color=team_color)

    db.session.add(team)
    db.session.commit()

    return success_response(
        team.to_dict(),
        "Team created successfully.",
        201
    )


@team_bp.route("/api/teams/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    team = Team.query.get(team_id)

    if not team:
        return error_response("Team not found.", 404)

    data = request_data()

    if "team_name" in data:
        team_name = clean_string(data["team_name"])

        if not team_name:
            return error_response("team_name is required.", 400)

        existing = Team.query.filter(
            func.lower(Team.team_name) == team_name.lower(),
            Team.team_id != team_id
        ).first()

        if existing:
            return error_response("Team name already exists.", 409)

        team.team_name = team_name

    if "team_color" in data:
        team_color = clean_string(data["team_color"])

        if not team_color:
            return error_response("team_color is required.", 400)

        team.team_color = team_color

    db.session.commit()

    return success_response(
        team.to_dict(),
        "Team updated successfully."
    )


@team_bp.route("/api/teams/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    team = Team.query.get(team_id)

    if not team:
        return error_response("Team not found.", 404)

    db.session.delete(team)
    db.session.commit()

    return success_response(
        {"team_id": team_id},
        "Team deleted successfully."
    )
