from flask_restplus import fields
from sample2.api.restplus import api

# NOTE : in FLASKRestplus things are missed up between api.model and api.parser
#        we have to define twice the same things depending it we want to use json for POST or querystring for GET
#        validation for input arguments
#        Should wait marshmallow integration in Flask-RESTPlus

operation_arg_json_model = api.model('Math operation arguments', {
    'a': fields.Integer(required=True, description='A number', example=1),
    'b': fields.Integer(required=True, description='A number', example=2),
})

operation_arg_parser = api.parser()
operation_arg_parser.add_argument('a', required=True, help='A number', type=int)
operation_arg_parser.add_argument('b', required=True, help='A number', type=int)
