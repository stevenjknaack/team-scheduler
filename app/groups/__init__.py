from flask import Blueprint

bp: Blueprint = Blueprint('groups', __name__)

from . import routes