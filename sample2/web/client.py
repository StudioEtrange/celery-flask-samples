import os, logging
from flask import Blueprint, render_template, url_for
#from flask_restplus.api import url_for


log = logging.getLogger(__name__)

web_root = os.path.abspath(os.path.dirname(__file__))

web = Blueprint('web', __name__, url_prefix='/web', template_folder=web_root + os.sep + 'templates')


# -------------- WEB PAGE ----------
@web.route('/', methods=['GET'])
def render_index():
    return render_template('index.html')
