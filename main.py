"""Module for creating the flask app"""

# System libraries

# Third-Party libraries
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restplus import Api
from flask_cors import CORS
from decouple import config as env_config

# middlewares
from api import api_blueprint
from api.middlewares import middleware_blueprint
from api.middlewares.base_validator import ValidationError

# Config
from config import config

# models
from api.models.database import db

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

    # Initialize migration script
    migrate = Migrate(app, db)

    return app


@api.errorhandler(ValidationError)
@middleware_blueprint.app_errorhandler(ValidationError)
def handle_exception(error):
    """Error handler called when a ValidationError is raised"""

    # response = jsonify(error.to_dict)
    # response.status_code = error.status_code
    #
    # return response

    return jsonify(error.to_dict), error.status_code

