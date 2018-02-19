import logging
import traceback
import os
from flask_restplus import Api
from sample2 import settings


log = logging.getLogger(__name__)

api = Api(version='1.0', title=os.environ['FLASK_APP_NAME'] + ' API',
          description='')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500
