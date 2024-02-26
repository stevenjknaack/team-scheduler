""" Defines routes related to teams """

from flask import Response, render_template, redirect, url_for, jsonify, session, request 
from ..extensions import db
from ..models.user import User
from ..models.team import Team
from ..models.membership import Membership
from ..teams import bp
from ..auth.decorators import login_required

@bp.route('/<int:team_id>') #TODO finish
@login_required
def go_to_team_page(team_id: int) -> str | Response:
    team_: Team = db.session.get(Team, team_id)
    return render_template('teams/team.html', username=session.get('username'), team=team_)

@bp.route('/partition_team_page')
@login_required #TODO implement this
def create_teams() -> Response:
    people_ = ["Tony", "Steven", "Georgia", "Dante", 
              "Anwita", "Kyle", "Tony1", "Tony2", 
              "Steve3n", "Geo42rgia", "Dan34te", 
              "Anw34ita", "Kyl34e", "T34ony"] 
    
    # Retrieve group_id from query parameters
    group_id_ = request.args.get('group_id')
    
    return render_template('teams/partition_teams.html', username=session.get('username'), people=people_, group_id=group_id_)

@bp.route('/manual_create_team_page')
@login_required
def manual_create_teams():
    group_id = request.args.get('group_id')

    # Ensure group_id is provided
    if not group_id:
        # Handle the case where group_id is not provided
        return redirect(url_for('some_default_route'))  # TODO Redirect to a default route or error page 

    # Query for all users in the specified group
    users_query = db.session.query(User).join(Membership).filter(Membership.group_id == group_id)
    users = users_query.all()

    # Extract usernames and emails
    people = [{'email': user.email, 'username': user.username} for user in users]

    return render_template('teams/manual_create_team.html', username=session.get('username'), people=people, group_id=group_id)


@bp.route('/generate_teams', methods=['POST'])
@login_required
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
    return Response(status=501) # TODO not implemented

@bp.route('/manual_create_teams', methods=['POST'])
@login_required
def create_team() -> str | Response:
    """
    Create a team manually and add participants.
    """
    # Parse incoming JSON data
    data = request.get_json()

    print("Received data:", data)  # Log the received data

    # Extract team details
    team_name = data.get('name')
    team_description = data.get('description')
    group_id = data.get('group_id')
    participants = data.get('participants')  # List of participant emails
    print(participants)

    # Create a new Team instance
    new_team = Team(group_id=group_id, name=team_name, description=team_description)

    try:
        # Add the new team to the session
        db.session.add(new_team)

        # Add participants to the team
        for email in participants:
            user = db.session.get(User, email)
            if user:
                new_team.members.append(user)
            else:
                # Handle the case where the user is not found
                print(f"User with email {email} not found")

        # Commit changes to the database
        db.session.commit()
        #print(f"Created team with ID {new_team.id}, Name {new_team.name}, Description {new_team.description}, Group ID {new_team.group_id}")

        return jsonify({"message": "Team created successfully", "team_id": new_team.id}), 201
    
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500