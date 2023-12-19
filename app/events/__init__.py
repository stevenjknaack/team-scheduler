from flask import Blueprint

bp: Blueprint = Blueprint('events', __name__, template_folder='templates', static_folder='static')

from . import routes