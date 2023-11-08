from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db import get_db

teams_blueprint = Blueprint('teams', __name__, template_folder='../../templates', static_folder='../../static')

"""
This method will use an algorithm to generate teams within a group, such as T_1->T_10 part of 
CS50Fall623. It will then send invitations to users to their respective teams which they will be
able to accept or deny. It inserts all the teams generated to the database, and once a user accepts
their invitation they will be put into the database under their team (see accept_invite method).
"""
@teams_blueprint.route('/teams', methods=['POST'])
def generate_teams():
    """ Get list of group participants as well as their time availability from database. """

    """ Insert into algorithm """

    """ Send invite to all users in group to their respective teams """

    """ return succesful Jquery """

