from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.team import Team


team_bp = Blueprint("team_bp", __name__)


@team_bp.route("/api/teams", methods=["GET"])
def get_teams():

    teams = Team.query.all()

    result = []

    for team in teams:
        result.append({
            "team_id": team.team_id,
            "team_name": team.team_name,
            "team_color": team.team_color
        })

    return jsonify(result)


@team_bp.route("/api/teams/<int:team_id>", methods=["GET"])
def get_team(team_id):

    team = Team.query.get_or_404(team_id)

    return jsonify({
        "team_id": team.team_id,
        "team_name": team.team_name,
        "team_color":team.team_color
    })


@team_bp.route("/api/teams", methods=["POST"])
def create_team():

    data = request.get_json()

    team = Team(
        team_name=data["team_name"],
        team_color=data["team_color"]
    )

    db.session.add(team)
    db.session.commit()

    return jsonify({
        "message": "Team created successfully"
    }), 201