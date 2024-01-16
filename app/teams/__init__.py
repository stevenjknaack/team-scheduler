from flask import Blueprint

bp: Blueprint = Blueprint('teams', __name__)

from . import routes