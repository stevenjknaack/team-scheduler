from flask import Blueprint

bp: Blueprint = Blueprint('events', __name__)

from . import routes