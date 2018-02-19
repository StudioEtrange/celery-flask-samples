import logging
from flask_restplus import Resource
#from flask import url_for

from sample2.api.restplus import api
from sample2.api.math.serializers import math_job
from sample2.api.math.parsers import operation_arg_json_model, operation_arg_parser
from sample2.api.math.endpoints.jobs import MathJobStatus
from sample2.business.math.tasks import add_task

log = logging.getLogger(__name__)
ns = api.namespace('math/add', description='Operations related to add')

# NOTE
# Headers documentation will be available only in next version of flask-RESTPlus
# api.response(...., headers={'Location','desc'})

# NOTE
# Flask.url_for('api.math/jobs_math_job')
# is equivalent to
# FlaskRestPlus.Api.url_for(MathJob)
# Both returns full URI http://host:port/api/math/jobs
# Cant find a way to get only /api/math/jobs
# like https://github.com/noirbizarre/flask-restplus/blob/master/tests/test_api.py


@ns.route('')
class AddJob(Resource):

    @ns.marshal_with(math_job)
    @ns.expect(operation_arg_parser)
    @ns.response(202, 'Job submitted.',headers={'Location': 'URL of job status'})
    def get(self):
        """
        Creates a new job.
        """
        request_args = operation_arg_parser.parse_args()
        result_task = add_task.apply_async(args=(request_args['a'], request_args['b']))
        return {'id' : result_task.task_id, 'status': result_task.state }, 202, {'Location': api.url_for(MathJobStatus,id=result_task.task_id)}

    @ns.marshal_with(math_job)
    @ns.expect(operation_arg_json_model)
    @ns.response(202, 'Job submitted.')
    def post(self):
        """
        Creates a new job.
        """
        request_args = api.payload
        result_task = add_task.apply_async(args=(request_args['a'], request_args['b']))
        return {'id' : result_task.task_id, 'status': result_task.state }, 202, {'Location': api.url_for(MathJobStatus,id=result_task.task_id)}
