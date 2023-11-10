from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db import get_db

groups_blueprint = Blueprint('groups', __name__, template_folder='../../templates', static_folder='../../static')