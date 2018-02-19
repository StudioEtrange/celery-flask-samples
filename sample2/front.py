import logging.config
import os
from flask import Flask, Blueprint
from sample2 import settings
from sample2.api.restplus import api
from sample2.api.math.endpoints.jobs import ns as math_jobs_namespace
from sample2.api.math.endpoints.add import ns as math_add_jobs_namespace
from sample2.api.math.endpoints.mul import ns as math_mul_jobs_namespace
from sample2.web.client import web as blueprint_web

project_root = os.path.abspath(os.path.dirname(__file__))
frontapp = Flask(os.environ['FLASK_APP_NAME'])
logging.config.fileConfig(project_root + os.sep + 'logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    #flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint_api = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint_api)
    api.add_namespace(math_jobs_namespace)
    api.add_namespace(math_add_jobs_namespace)
    api.add_namespace(math_mul_jobs_namespace)
    flask_app.register_blueprint(blueprint_api)

    flask_app.register_blueprint(blueprint_web)

if __name__ == "__main__":
    initialize_app(frontapp)
    frontapp.debug = settings.FLASK_DEBUG
    frontapp.run(host = '0.0.0.0', port = int(os.environ["FRONTEND_PORT"]))
