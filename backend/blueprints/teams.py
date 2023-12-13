""" Defines routes related to teams """

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, Response, current_app
from ..models import *

teams_blueprint: Blueprint = Blueprint('teams', __name__, 
                            template_folder='../../templates', 
                            static_folder='../../static')

@teams_blueprint.route('/team')
def go_to_team_page() -> str | Response:
    return render_template('team.html')

@teams_blueprint.route('/generate_teams', methods=['POST'])
def generate_teams() -> Response :
    """
    This method will use an algorithm to generate teams within a group, such as T_1->T_10 part of 
    CS50Fall623. It will then send invitations to users to their respective teams which they will be
    able to accept or deny. It inserts all the teams generated to the database, and once a user accepts
    their invitation they will be put into the database under their team (see accept_invite method).
    """
    # Get list of group participants as well as their time availability from database. 

    # Insert into algorithm 

    # Send invite to all users in group to their respective teams 

    # return succesful Jquery 
    return Response(status=501) # not implemented

@teams_blueprint.route('/manual_create_teams', methods=['POST'])
def create_team() -> str | Response:
    """
    This Method will allow for creating a team manually, without needing time availabilty. A user who 
    creates a team can give a name to the team and insert people manually into it by providing their email.
    Other USers who have been invited will get a notification which will allow them to accept or deny invitation.
    """
    # Creates a team with team name and size. 
    # Get information from group participant via email from DB
    # Commit team to DB 
    # Commit participants into DB 
    # Return succesful JQuery 
    return Response(status=501) # not implemented
  
