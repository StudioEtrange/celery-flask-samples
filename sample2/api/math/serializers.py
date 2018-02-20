from flask_restplus import fields
from sample2.api.restplus import api



math_job = api.model('Math job', {
    'id' : fields.String(required=True, description='job id'),
    'status': fields.String(required=False, description='job status',default=None, example='STARTED', enum=('SUCCESS','PENDING','ERROR','STARTED','FAILURE','RETRY','REVOKED')),
    'result': fields.String(required=False, description='job result',default=None),
    'desc' : fields.String(required=False, description='descriptive information', default='')
})
