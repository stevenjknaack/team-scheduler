from flask import Blueprint

bp: Blueprint = Blueprint('main', __name__, template_folder='templates', static_folder='static')

from . import routes