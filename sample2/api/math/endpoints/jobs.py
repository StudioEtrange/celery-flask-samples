import logging
from flask import request
from flask_restplus import Resource
from celery import states
from celery.result import AsyncResult

from sample2.api.math.serializers import math_job
from sample2.api.restplus import api
from sample2.back import backapp

log = logging.getLogger(__name__)
ns = api.namespace('math/jobs', description='Operations related to math jobs')


def error(result_task):
    """
    generic error return
    """
    try:
        cause = 'task state : {} - '.format(state) + result_task.info.get('error')
    except Exception as e:
        cause = 'task state : {} - '.format(state) + 'Unknown error occurred'
    return { 'id': result_task.task_id, 'status':'ERROR', 'desc': cause }, 500



@ns.route('/status/<string:id>')
@ns.param('id','A Job ID')
@ns.response(500, 'Job error.')
class MathJobStatus(Resource):

    @ns.marshal_with(math_job)
    @ns.response(303, 'Job successfully finished.')
    @ns.response(200, 'Job unknown or not yet started.')
    def get(self, id):
        """
        Return status of a queued job.
        """
        result_task = AsyncResult(id = id, app = backapp)
        state = result_task.state

        if state == states.STARTED:
            return { 'id':result_task.task_id, 'status': state }, 200
        # task still pending or unknown
        elif state == states.PENDING:
            return { 'id':result_task.task_id, 'status': state }, 200
        elif state == states.SUCCESS:
            return { 'id':result_task.task_id, 'status': state }, 303, {'Location': api.url_for(MathJobResult,id=result_task.task_id)}
        else:
            return error(result_task)


@ns.route('/result/<string:id>')
@ns.param('id','A Job ID')
@ns.response(500, 'Job error.')
class MathJobResult(Resource):

    @ns.marshal_with(math_job)
    @ns.response(404, 'Result do not exists.')
    @ns.response(200, 'Return result.')
    def get(self, id):
        """
        Return result of a job.
        """
        result_task = AsyncResult(id = id, app = backapp)
        state = result_task.state

        # tasks finished so result exists
        if state == states.SUCCESS:
            return { 'id': result_task.task_id, 'status': state, 'result': result_task.get(timeout=1.0)}, 200
        # task still pending or unknown - so result do not exists
        elif state == states.PENDING:
            return { 'id': result_task.task_id, 'status': state }, 404
        # task started but result do not exists yet
        elif state == states.STARTED:
            return { 'id': result_task.task_id, 'status': state }, 404
        else:
            return error(result_task)


    @ns.marshal_with(math_job)
    @ns.response(404, 'Result do not exists.')
    @ns.response(200, 'Result deleted.')
    def delete(self, id):
        """
        Delete a result of a job.
        """
        result_task = AsyncResult(id = id, app = backapp)
        state = result_task.state

        # tasks finished so result exists
        if state == states.SUCCESS:
            try:
                result_task.forget()
            except Exception as e:
                return error(result_task)
            return { 'id': result_task.task_id, 'desc': 'result for job {} deleted'.format(result_task.task_id) }, 200
        # task still pending or unknown - so result do not exists
        elif state == states.PENDING:
            return { 'id': result_task.task_id, 'status': state }, 404
        # task started but result do not exists yet
        elif state == states.STARTED:
            return { 'id': result_task.task_id, 'status': state }, 404
        else:
            return error(result_task)
