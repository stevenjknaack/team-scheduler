from flask import Blueprint

bp: Blueprint = Blueprint('profile', __name__)

from . import routes