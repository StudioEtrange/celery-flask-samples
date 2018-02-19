import os
from flask import Flask, url_for, jsonify, request, make_response, render_template
from celery import Celery, states
from celery.result import AsyncResult
from flask_cors import CORS, cross_origin

from sample1.tasks import add_task, mul_task
from sample1.back import backapp

project_root = os.path.abspath(os.path.dirname(__file__))

frontapp = Flask(os.environ['FLASK_APP_NAME'],template_folder=project_root + os.sep + 'templates')
CORS(frontapp)

# -------------- WEB PAGE ----------
@frontapp.route('/', methods=['GET'])
def render_index():
    return render_template('index.html', title=frontapp.name)

# -------------- API --------------
@frontapp.route('/add', methods=['GET','POST'])
def add():
    # https://stackoverflow.com/a/16664376
    # pure json body with json content type
    if request.is_json:
        data = request.get_json()
        a = int(data['a'])
        b = int(data['b'])
    else:
        # HTML form
        if request.method == 'POST':
            a = int(request.form['a'])
            b = int(request.form['b'])
        else:
            # Querystring
            a = request.args.get('a',type=int)
            b = request.args.get('b',type=int)

    result_task = add_task.apply_async(args=(a,b))
    return make_response(jsonify({'task_id': result_task.task_id}))

@frontapp.route('/mul', methods=['GET','POST'])
def mul():
    # https://stackoverflow.com/a/16664376
    # pure json body with json content type
    if request.is_json:
        data = request.get_json()
        a = int(data['a'])
        b = int(data['b'])
    else:
        # HTML form
        if request.method == 'POST':
            a = int(request.form['a'])
            b = int(request.form['b'])
        else:
            # Querystring
            a = request.args.get('a',type=int)
            b = request.args.get('b',type=int)

    result_task = mul_task.apply_async(args=(a,b))
    return make_response(jsonify({'task_id': result_task.task_id}))


@frontapp.route('/task/<task_id>', methods=['GET'])
def check_generic_task(task_id):
    task = AsyncResult(id = task_id, app = backapp)
    task_info = get_task_info(task)
    return make_response(task_info)

@frontapp.route('/task/add/<task_id>', methods=['GET'])
def check_add_task(task_id):
    task = add_task.AsyncResult(task_id)
    task_info = get_task_info(task)
    return make_response(task_info)


@frontapp.route('/task/mul/<task_id>', methods=['GET'])
def check_mul_task(task_id):
    task = mul_task.AsyncResult(task_id)
    task_info = get_task_info(task)
    return make_response(task_info)



def get_task_info(task):
    state = task.state
    response = {}
    response['state'] = state
    if state == states.SUCCESS:
        response['result'] = task.get()
    elif state == states.FAILURE:
        try:
            response['error'] = task.info.get('error')
        except Exception as e:
            response['error'] = 'Unknown error occurred'
    return jsonify(response)

# http://docs.celeryproject.org/en/latest/userguide/monitoring.html
@frontapp.route('/tasks', methods=['GET'])
def list_tasks():
    result={}
    result['active'] = backapp.control.inspect().active()
    result['scheduled'] = backapp.control.inspect().scheduled()
    result['reserved'] = backapp.control.inspect().reserved()
    result['revoked'] = backapp.control.inspect().revoked()
    result['registered'] = backapp.control.inspect().registered()
    return make_response(jsonify(result))

if __name__ == '__main__':
    frontapp.debug = True
    frontapp.run(host = '0.0.0.0', port = int(os.environ["FRONTEND_PORT"]))
