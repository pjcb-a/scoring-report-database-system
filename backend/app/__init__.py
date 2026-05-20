from flask import Flask
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from app.config import Config
from app.extensions import db, migrate


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import (
        event,
        sport,
        scoring_type,
        event_sport,
        team,
        game,
        game_score,
        criteria,
        judge,
        score_component
    )

    from app.routes import (
        event_bp,
        sport_bp,
        scoring_type_bp,
        team_bp,
        game_bp,
        game_score_bp,
        criteria_bp,
        judge_bp,
        score_component_bp,
        event_sport_bp,
        report_bp
    )

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

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()

        from app.routes.utils import error_response

        return error_response(
            "Database constraint violated.",
            409,
            [str(error.orig)]
        )

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        from app.routes.utils import error_response

        return error_response(
            error.description,
            error.code
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        db.session.rollback()

        from app.routes.utils import error_response

        return error_response(
            "Unexpected server error.",
            500,
            [str(error)]
        )

    return app
