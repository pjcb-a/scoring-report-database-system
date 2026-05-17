from flask import Flask
from flask_cors import CORS

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
        team_bp,
        game_bp,
        game_score_bp,
        criteria_bp,
        judge_bp,
        score_component_bp,
        event_sport_bp,
        report_bp
    )
    
    return app