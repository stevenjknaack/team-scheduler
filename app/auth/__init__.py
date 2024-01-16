from flask import Blueprint

bp: Blueprint = Blueprint('auth', __name__)

from . import routes
from . import decorators