import logging
from flask_restplus import Resource

from sample2.api.restplus import api
from sample2.api.math.serializers import math_job
from sample2.api.math.parsers import operation_arg_json_model, operation_arg_parser
from sample2.api.math.endpoints.jobs import MathJobStatus
from sample2.business.math.tasks import mul_task

log = logging.getLogger(__name__)
ns = api.namespace('math/mul', description='Operations related to add')

@ns.route('')
class MulJob(Resource):

    @ns.marshal_with(math_job)
    @ns.expect(operation_arg_parser)
    @ns.response(202, 'Job submitted.',headers={'Location': 'URL of job status'})
    def get(self):
        """
        Creates a new job.
        """
        request_args = operation_arg_parser.parse_args()
        result_task = mul_task.apply_async(args=(request_args['a'], request_args['b']))
        return {'id' : result_task.task_id, 'status': result_task.state }, 202, {'Location': api.url_for(MathJobStatus,id=result_task.task_id)}

    @ns.marshal_with(math_job)
    @ns.expect(operation_arg_json_model)
    @ns.response(202, 'Job submitted.')
    def post(self):
        """
        Creates a new job.
        """
        request_args = api.payload
        result_task = mul_task.apply_async(args=(request_args['a'], request_args['b']))
        return {'id' : result_task.task_id, 'status':result_task.state }, 202, {'Location': api.url_for(MathJobStatus,id=result_task.task_id)}
