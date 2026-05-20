from .event_routes import event_bp
from .sport_routes import sport_bp
from .scoring_type_routes import scoring_type_bp
from .team_routes import team_bp
from .game_routes import game_bp
from .game_score_routes import game_score_bp
from .criteria_routes import criteria_bp
from .judge_routes import judge_bp
from .score_component_routes import score_component_bp
from .event_sport_routes import event_sport_bp
from .report_routes import report_bp


def register_blueprints(app):

    """
    --------------------------------------------------------------------------
    REGISTER ALL BLUEPRINTS
    --------------------------------------------------------------------------
    """

    app.register_blueprint(event_bp)

    app.register_blueprint(sport_bp)

    app.register_blueprint(scoring_type_bp)

    app.register_blueprint(team_bp)

    app.register_blueprint(game_bp)

    app.register_blueprint(game_score_bp)

    app.register_blueprint(criteria_bp)

    app.register_blueprint(judge_bp)

    app.register_blueprint(score_component_bp)

    app.register_blueprint(event_sport_bp)

    app.register_blueprint(report_bp)