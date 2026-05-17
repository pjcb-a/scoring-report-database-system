from flask import Blueprint


report_bp = Blueprint("report_bp", __name__)


@report_bp.route("/api/reports/game-results")
def game_results_report():
    return {
        "message": "Game results report endpoint"
    }


@report_bp.route("/api/reports/component-scores")
def component_scores_report():
    return {
        "message": "Component scores report endpoint"
    }