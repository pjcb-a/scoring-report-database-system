from flask import Flask

from flask_cors import CORS

from app.config import Config

from app.extensions import db, migrate

from app.routes import register_blueprints


def create_app():

    app = Flask(__name__)

    """
    --------------------------------------------------------------------------
    LOAD CONFIGURATION
    --------------------------------------------------------------------------
    """

    app.config.from_object(Config)

    """
    --------------------------------------------------------------------------
    INITIALIZE EXTENSIONS
    --------------------------------------------------------------------------
    """

    db.init_app(app)

    migrate.init_app(app, db)

    CORS(app)

    """
    --------------------------------------------------------------------------
    IMPORT MODELS
    IMPORTANT:
    Required for Flask-Migrate detection
    --------------------------------------------------------------------------
    """

    from app import models

    """
    --------------------------------------------------------------------------
    REGISTER ROUTES
    --------------------------------------------------------------------------
    """

    register_blueprints(app)

    """
    --------------------------------------------------------------------------
    ROOT ROUTE
    --------------------------------------------------------------------------
    """

    @app.route("/")

    def home():

        return {

            "success": True,

            "message":
            "Sports Reporting Database System API Running"
        }

    return app