""" Defines group related routes """

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, Response, current_app
from models import *
from blueprints.events import create_event, add_participant_to_event

groups_blueprint: Blueprint = Blueprint('groups', __name__, 
                                        template_folder='../../templates', 
                                        static_folder='../../static')

@groups_blueprint.route('/group')
def go_to_group_page() -> Response:
    return render_template('group.html')

@groups_blueprint.route('/create_team')
def create_teams() -> Response:
    people = ["Tony", "Steven", "Georgia", "Dante", "Anwita", "Kyle", "Tony1", "Tony2", "Steve3n", "Geo42rgia", "Dan34te", "Anw34ita", "Kyl34e", "T34ony"]  # List of people
    return render_template('create_teams.html', people=people)

@groups_blueprint.route('/create_group', methods=['GET', 'POST'])
def create_group() -> Response:
    """ 
    This method will be made for creating groups. It'll allow for someone to make a group such as 
    CS506Fall23. It will get information such as group name and description. An SQL query will be
    executed to save the group to the database, and then once done it will redirect to home page.
    """
    # Step1: get information from the user such as event name and description.
    group_name: str = request.args.get('groupName')
    group_description: str = request.args.get('groupDescription')
    
    
    # Step2: create group and make the user a member
    new_group: Group = Group(group_name, group_description)
    email: str = session.get('email')
    new_membership: Membership = Membership(email, None, 'owner')
    new_group.memberships.append(new_membership)

    current_app.db.session.add_all([new_group, new_membership])
    current_app.db.session.commit()

    # Step3: redirect to home page. 
    return redirect(url_for('auth.home'))

def is_group_admin(group_id: int, user_id: int) -> bool:
    """ 
    determines if the user of user_id an admin of 
        the group of group_id #TODO
    """
    # Connect to the database
    db = None
    cursor = db.cursor()

    try:
        # Query to check if the user is the admin of the group
        query = "SELECT admin_id FROM groups WHERE group_id = %s"
        cursor.execute(query, (group_id,))
        admin_id = cursor.fetchone()

        # Check if the user_id matches the admin_id
        if admin_id and user_id == admin_id[0]:
            return True  # The user is the admin of the group
        else:
            return False  # The user is not the admin of the group

    except Exception as e:
        # Handle any potential errors, such as database connection issues
        print(f"Error checking group admin: {str(e)}")
        return False  # Return False to indicate that an error occurred

    finally:
        cursor.close()
        db.close()

def get_group_members(group_id: int) -> List[int] :
    """get the group members correlated with group_id"""
    # Connect to the database
    db = None
    cursor = db.cursor()

    try:
        # Query to retrieve a list of member IDs for the specified group
        query = "SELECT user_id FROM group_members WHERE group_id = %s"
        cursor.execute(query, (group_id,))
        member_ids = [result[0] for result in cursor.fetchall()]

        return member_ids  # Return a list of member IDs

    except Exception as e:
        # Handle any potential errors, such as database connection issues
        print(f"Error retrieving group members: {str(e)}")
        return []  # Return an empty list to indicate that an error occurred

    finally:
        cursor.close()
        db.close()

@groups_blueprint.route('/send-invitations', methods=['POST'])
def send_invitations() -> Response :
    """ Sends group invitations to users """

    # Get JSON data sent from the frontend
    data = request.get_json()

    # Extract email addresses
    emails = data.get('emails', [])

    
    # placeholder
    event_id = 5

    # connect to database
    db = None

    # create a cursor 
    cursor = db.cursor()

    for email in emails:
        query = "INSERT INTO invitee (event_id, email) VALUES (%s, %s)"
        values = (event_id, email)
        cursor.execute(query, values)
        db.commit()
    
    # close cursor and database
    cursor.close()
    db.close()

    # TODO: Process the emails, e.g., send invitation emails, save to the database, etc.
    # For now, let's just print them for demonstration purposes
    print(emails)

    return jsonify(status='success', message='Invitations sent successfully!')

#@events_blueprint.route('/group/<int:group_id>/create-event', methods=['POST'])
def create_group_event(group_id: int) -> Response:
    """ Create a group level event """

    # Authenticate the user and check if they are the group admin
    current_user_id = session.get('user_id')
    if not is_group_admin(group_id, current_user_id):
        return jsonify({"status": "error", "message": "You do not have permission to create group events."}), 403

    # Get event details from the request
    data = request.get_json()
    event_name = data.get('event_name')
    event_description = data.get('event_description')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    recurring = data.get('recurring')  # True or False

    # Retrieve the list of group members
    group_members = get_group_members(group_id)

    if not group_members:
        return jsonify({"status": "error", "message": "No group members found."}), 404

    # Create the event in the database
    event_id = create_event(event_name, event_description, start_date, end_date, recurring)

    if event_id:
        # Add all group members as event participants
        for member_id in group_members:
            add_participant_to_event(event_id, member_id)

        return jsonify({"status": "success", "message": "Group event created successfully."}), 201
    else:
        return jsonify({"status": "error", "message": "Event creation failed. Please check your input."}), 500