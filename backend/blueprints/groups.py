""" Defines group related routes """

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, Response, current_app
from ..models import *
from flask_mail import Mail, Message
from ..blueprints.events import create_event, add_participant_to_event
from sqlalchemy import select

from sqlalchemy.orm import selectinload

groups_blueprint: Blueprint = Blueprint('groups', __name__, 
                                        template_folder='../../templates', 
                                        static_folder='../../static')




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

@groups_blueprint.route('/get-group-id', methods=['GET'])
def get_group_id() -> Response :
    """ Retreives a group_id given a specified group name """
    # get the group name from the request parameters
    group_name = request.args.get('group_name')

    # query the database to find group_id for specified group_name
    db = None
    cursor = db.cursor
    cursor.execute("SELECT id from 'group' WHERE name = %s", (group_name,))
    result = cursor.fetchone()

    if result: 
        group_id = result[0]
        return jsonify({'group_id': group_id}) # success: return group_id
    else: 
        return jsonify({'error': 'Group not found'}), 404 # failure: return error response

@groups_blueprint.route('/send-invitations/<int:group_id>', methods=['POST'])
def send_invitations(group_id: int) -> Response :
   """ Sends group invitations to users via email using Flask-Mail API """
   # get Mail instance
   mail = Mail(current_app)

   # Get JSON data (list of emails), sent from the frontend
   data = request.get_json()

   # Extract email addresses
   emails = data.get('emails', [])

   for email in emails :
       # check if user exists
       if not current_app.db.session.get(User, email) :
           continue
       # check if the user is already a member of the group
       existing_membership = current_app.db.session.get(Membership, (email, group_id))

       # if user is not already a member, add them as an invitee
       if not existing_membership:
           new_membership = Membership(user_email=email, group_id=group_id, role='invitee')

           # add the new invitee to the session and commit
           current_app.db.session.add(new_membership)
           current_app.db.session.commit()

   # TODO: Process the emails, e.g., send invitation emails, save to the database, etc.
   # For now, let's just print them for demonstration purposes
   #print(emails)

   # sending invitation email functionality through Flask-Mail API

   # for each email in email list, send an invitation email 
   """
   for email in emails:
       message = Message(subject='You have been invited to a group!', recipients=[email])
       message.body = f'You are invited to a group with ID {group_id}. Please log into the Scheduler App to accept your invitation!'
       try:
           mail.send(message)
       except Exception as e:
           print(f'Error sending invitation email to {email}: {str(e)}')
        """
           

   return jsonify(status='success', message='Invitations sent successfully!'), 201

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
    recurring = data.get('recurring')  # TODO: false type, look at the db and start_day and end_date

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
        
@groups_blueprint.route('/join_group/', methods = ['GET', 'POST'])
def join_group()-> Response:
    """ This method is being written to handle the functionality of joining a group from a members side, by inputting
        a valid group ID. The user will still need to be allowed in by the owner/admins of the group, and we assume the
        user has been sent the valid group ID, and is a valid member.
    """
    user_email = session.get('email')
    # step 1: check that group_id is valid and exists, and that user is not member of the group else show error message
    group_id = request.form.get('groupCode')
    valid_group =  current_app.db.session.get(Group, group_id)
    membership = current_app.db.session.query(Membership).filter_by(group_id=group_id, user_email=user_email).first()
    print("group_id:", group_id)
    print("membership:", membership)
    if((not valid_group) or membership):   
        return jsonify(status='error',  message='Group ID incorrect or group does not exist'), 401
    # step2: if valid, send notification to group admin where they can accept or deny the request
    else:
        # Add user to database with role requester
        new_membership = Membership(user_email=user_email, group_id=group_id, role='requester')
        # Get Owner of groups ID
        # membership = current_app.db.session.query(Membership).filter_by(group_id=group_id).first()
        # owner = membership.user_email
        # # Send message to owner of group with requester ID
        # group_name = valid_group.name
        # message = Message(subject='A new User wants to join your group!', recipients=[owner])
        # message.body = f'User {user_email} wants to join group {group_name} with ID {group_id}. Please log into the Scheduler App to review this request!'
        current_app.db.session.add(new_membership)
        current_app.db.session.commit()
        # try:
        #     mail.send(message)
        # except Exception as e:
        #     print(f'Error sending request, try again please')
        return redirect(url_for('auth.home'))
    # step 3: if step 1 and 2 were completed regularly, close modal, reload home page.

@groups_blueprint.route('/group/<int:group_id>') 
def group_page(group_id):
    """ This method is used to redirect from the home page to a group page, when the user clicks
        on a group in their home page. The user must be a part of the group, whether a member or admin,
        for the box to show up. It takes the groupID that matches the group, and embeds it in the URL, to identify 
        which group it is for other actions in the future (like creating a group event).

        :author: Dante Katz Andrade
        :version: 2023.10.19
        """
    if 'email' not in session:
        return redirect(url_for('auth.home'))
    user_email = session['email']

    # Fetch the group and its teams with eager loading to optimize queries
    group = current_app.db.session.query(Group).options(selectinload(Group.teams)).get(group_id)

    if not group:
        return redirect(url_for('auth.home'))  # Group not found

    # Check that user is a member of the group
    is_member = current_app.db.session.execute(select(Membership).filter_by(user_email=user_email, group_id=group_id)).scalar()
    if not is_member:
        return redirect(url_for('auth.home'))  # User is not a member of the group

    # Prepare team data
    team_data = []
    for team in group.teams:
        members = [member.username for member in team.members]
        team_data.append({'name': team.name, 'members': members})


    user_events_result = current_app.db.session.scalars(select(Event).filter_by(group_id=group_id))
    user_events = [event for event in user_events_result]

    return render_template('group.html', group=group, user_events=user_events, group_id=group_id, teams=team_data)
    
@groups_blueprint.route('/delete_from_group/<int:group_id>', methods=['POST'])
def delete_user_from_group(group_id: int) -> Response :
    """
    Deletes the current user from a specified group

    :group_id: the id of the group to delete the current user from
    """
    # get user email from session
    user_email: str | None = session.get('email')

    # get and validate membership
    membership: Membership = current_app.db.session.get(Membership, (user_email, group_id))
    
    if not membership :
        return jsonify(status='error', message='user is not in group'), 401
    
    # delete user and return successful
    current_app.db.session.delete(membership)
    current_app.db.session.commit()

    return jsonify(status='success'), 201

@groups_blueprint.route('/change_group_role/<int:group_id>/<string:role>', methods=['POST'])
def change_user_group_role(group_id: int, role: str) -> Response :
    """
    Update a user's role in a group

    :group_id: the id of the group to change the current user's role in
    """
    # get user email from session
    user_email: str | None = session.get('email')

    # get and validate membership
    membership: Membership = current_app.db.session.get(Membership, (user_email, group_id))
    
    if not membership :
        return jsonify(status='error', message='user is not in group'), 401
    
    # update membership role
    membership.role = role
    current_app.db.session.commit()

    # return success
    return jsonify(status='success'), 201
    

@groups_blueprint.route('/delete-group/<int:group_id>', methods=['DELETE'])
def delete_group(group_id: int) -> Response:
    """
    This method deletes groups. It checks that the group is owned by the active user.
    """
    # Authenticate the user and check if they are the group admin
    user_email: str = session.get('email')
    membership = current_app.db.session.query(Membership).filter_by(user_email=user_email, group_id=group_id).first()

    # Check if the user is the owner of the group
    if membership and membership.role == 'owner':
        db_session = current_app.db.session
        # Query the group to delete
        group = db_session.get(Group, group_id)
        try:
            # Delete associated memberships
            for membership in group.memberships:
                db_session.delete(membership)

            # Delete the group
            db_session.delete(group)

            # Commit changes to the database
            db_session.commit()
            return jsonify(status='success')

        except SQLAlchemyError as e:
            # Print failure
            print(f"Exception during commit")
            # Rollback changes to avoid leaving the database in an inconsistent state
            db_session.rollback()  
            return jsonify(status='fail', error='Error during deletion'), 500
    
    # If the user is not the owner, do not delete
    return jsonify(status='fail')