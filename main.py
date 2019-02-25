"""Module for creating the flask app"""

# System libraries

# Third-Party libraries
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restplus import Api
from flask_cors import CORS
from decouple import config as env_config
from marshmallow import ValidationError as MarshmallowValidationError

# middlewares
from api import api_blueprint
from api.middlewares import middleware_blueprint
from api.middlewares.base_validator import ValidationError

# Config
from config import config

# models
from api.models.database import db
from api.models.base.base_model_exception import BaseModelException

config_name = env_config('FLASK_ENV', 'production')
api = Api(api_blueprint, doc=False)


def initialize_errorhandlers(application):
    """Initialize error handlers"""

    application.register_blueprint(middleware_blueprint)
    application.register_blueprint(api_blueprint)


def create_app(config=config[config_name]):
    """creates a flask app object from a config object"""

    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)

    # Initialize error handlers
    initialize_errorhandlers(app)

    # Bind app to database
    db.init_app(app)

    # import all models
    from api.models import User

    # import views
    import api.views

    # Initialize migration script
    migrate = Migrate(app, db)

    return app


@api.errorhandler(MarshmallowValidationError)
@middleware_blueprint.app_errorhandler(MarshmallowValidationError)
def handle_marshmallow_exception(error):
    """Error handler called when a marshmallow ValidationError is raised"""

    error_message = {
        'message': 'An error occurred',
        'status': 'error',
        'errors': error.messages
    }
    return jsonify(error_message), 400


@api.errorhandler(BaseModelException)
@middleware_blueprint.app_errorhandler(BaseModelException)
def handle_model_exception(exception):
    """Error handler called when a models error is raised"""

    return jsonify(exception.errors), exception.status_code


@api.errorhandler(ValidationError)
@middleware_blueprint.app_errorhandler(ValidationError)
def handle_exception(error):
    """Error handler called when a ValidationError is raised"""

    return jsonify(error.error), 400


