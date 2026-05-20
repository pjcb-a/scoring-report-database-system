from flask import Blueprint

from app.models.game_score import GameScore
from app.models.score_component import ScoreComponent
from app.models.team import Team
from app.routes.utils import success_response


report_bp = Blueprint("report_bp", __name__)


def game_score_report_row(score):
    data = score.to_dict()
    data["start_date"] = (
        score.game.start_date.isoformat()
        if score.game and score.game.start_date
        else None
    )
    data["game_status"] = score.game.game_status if score.game else None
    data["venue_name"] = score.game.venue_name if score.game else None

    return data


@report_bp.route("/api/reports", methods=["GET"])
@report_bp.route("/api/reports/game-results", methods=["GET"])
def game_results_report():
    scores = GameScore.query.order_by(
        GameScore.game_id.asc(),
        GameScore.rank_position.asc().nullslast(),
        GameScore.score_value.desc()
    ).all()

    return success_response(
        [game_score_report_row(score) for score in scores],
        "Game results report generated successfully."
    )


@report_bp.route("/api/reports/winners", methods=["GET"])
def winners_report():
    scores = GameScore.query.filter_by(isWinner=True).order_by(
        GameScore.game_id.asc(),
        GameScore.rank_position.asc().nullslast()
    ).all()

    return success_response(
        [game_score_report_row(score) for score in scores],
        "Winners report generated successfully."
    )


@report_bp.route("/api/reports/rankings", methods=["GET"])
def rankings_report():
    scores = GameScore.query.order_by(
        GameScore.game_id.asc(),
        GameScore.rank_position.asc().nullslast(),
        GameScore.score_value.desc()
    ).all()

    return success_response(
        [game_score_report_row(score) for score in scores],
        "Rankings report generated successfully."
    )


@report_bp.route("/api/reports/participation", methods=["GET"])
def participation_report():
    teams = Team.query.order_by(Team.team_name.asc()).all()
    report = []

    for team in teams:
        report.append({
            "team_id": team.team_id,
            "team_name": team.team_name,
            "team_color": team.team_color,
            "games_played": len(team.game_scores),
            "wins": len([
                score
                for score in team.game_scores
                if score.isWinner
            ])
        })

    return success_response(
        report,
        "Participation report generated successfully."
    )


@report_bp.route("/api/reports/judging-summary", methods=["GET"])
@report_bp.route("/api/reports/component-scores", methods=["GET"])
def judging_summary_report():
    components = ScoreComponent.query.order_by(
        ScoreComponent.score_component_id.desc()
    ).all()

    return success_response(
        [component.to_dict() for component in components],
        "Judging summary report generated successfully."
    )


@report_bp.route("/api/reports/history", methods=["GET"])
def historical_report():
    scores = GameScore.query.order_by(GameScore.game_score_id.desc()).all()

    return success_response(
        [game_score_report_row(score) for score in scores],
        "Historical report generated successfully."
    )
