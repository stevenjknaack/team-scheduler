""" Defines group related routes """

from flask import render_template, request, redirect, url_for, session, jsonify, Response
from ..extensions import db, mail
from ..models.user import User
from ..models.membership import Membership
from ..models.event import Event
from ..models.group import Group
from flask_mail import Message
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..groups import bp

@bp.route('/<int:group_id>') 
def group_page(group_id: int) -> Response | str :
    """ This method is used to redirect from the home page to a group page, when the user clicks
        on a group in their home page. The user must be a part of the group, whether a member or admin,
        for the box to show up. It takes the groupID that matches the group, and embeds it in the URL, to identify 
        which group it is for other actions in the future (like creating a group event).

        :author: Dante Katz Andrade
        :version: 2023.10.19
        """
    if 'email' not in session:
        return redirect(url_for('main.home'))
    user_email = session['email']

    # Fetch the group and its teams with eager loading to optimize queries
    group = db.session.query(Group).options(selectinload(Group.teams)).get(group_id)

    if not group:
        return redirect(url_for('main.home'))  # Group not found

    # Check that user is a member of the group
    is_member = db.session.execute(select(Membership).filter_by(user_email=user_email, group_id=group_id)).scalar()
    if not is_member:
        return redirect(url_for('main.home'))  # User is not a member of the group

    # Prepare team data
    team_data = []
    for team in group.teams:
        members = [member.username for member in team.members]
        team_data.append({'id': team.id, 'name': team.name, 'members': members})


    user_events_result = db.session.scalars(select(Event).filter_by(group_id=group_id))
    user_events = [event for event in user_events_result]
    print(user_events)
    return render_template('group.html', username=session.get('username'), group=group, user_events=user_events, group_id=group_id, teams=team_data)

@bp.route('/create_group', methods=['GET', 'POST'])
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

    db.session.add_all([new_group, new_membership])
    db.session.commit()

    # Step3: redirect to home page. 
    return redirect(url_for('main.home'))

@bp.route('/send-invitations/<int:group_id>', methods=['POST'])
def send_invitations(group_id: int) -> Response :
   """ Sends group invitations to users via email using Flask-Mail API """
   # Get JSON data (list of emails), sent from the frontend
   data = request.get_json()

   # Extract email addresses
   emails = data.get('emails', [])

   for email in emails :
       # check if user exists
       if not db.session.get(User, email) :
           continue
       # check if the user is already a member of the group
       existing_membership = db.session.get(Membership, (email, group_id))

       # if user is not already a member, add them as an invitee
       if not existing_membership:
           new_membership = Membership(user_email=email, group_id=group_id, role='invitee')

           # add the new invitee to the session and commit
           db.session.add(new_membership)
           db.session.commit()

   # for each email in email list, send an invitation email 
   group = db.session.get(Group, group_id)
   for email in emails:
       message_body = f'You are invited to {f'group {group.name}' or 'an unnamed group'} with ID {group.id}.' +\
                     '\nPlease log into the Scheduler App to accept your invitation!'
       message = Message(subject=f'Invitation to group {group.id}!', body=message_body, recipients=[email])
       
       try:
           mail.send(message)
       except Exception as e:
           print(f'Error sending invitation email to {email}: {str(e)}')

   return jsonify(status='success', message='Invitations sent successfully!'), 201
        
@bp.route('/join_group/', methods = ['GET', 'POST'])
def join_group()-> Response:
    """ This method is being written to handle the functionality of joining a group from a members side, by inputting
        a valid group ID. The user will still need to be allowed in by the owner/admins of the group, and we assume the
        user has been sent the valid group ID, and is a valid member.
    """
    user_email = session.get('email')
    # step 1: check that group_id is valid and exists, and that user is not member of the group else show error message
    group_id = request.form.get('groupCode')
    valid_group =  db.session.get(Group, group_id)
    membership = db.session.query(Membership).filter_by(group_id=group_id, user_email=user_email).first()
    membership = db.session.query(Membership).filter_by(group_id=group_id, user_email=user_email).first()
    print("group_id:", group_id)
    print("membership:", membership)
    if((not valid_group) or membership):   
        return jsonify(status='error',  message='Group ID incorrect or group does not exist'), 401
    # step2: if valid, send notification to group admin where they can accept or deny the request
    else:
        # Add user to database with role requester
        print(user_email)
        membership = db.session.query(Membership).filter_by(group_id=group_id).first()
        owner = membership.user_email
        print(owner)
        new_membership = Membership(user_email=user_email, group_id=group_id, role='requester')
        # Get Owner of groups ID
        #membership = current_app.db.session.query(Membership).filter_by(group_id=group_id).first()
        #owner = membership.user_email
        # # Send message to owner of group with requester ID
        # group_name = valid_group.name
        # message = Message(subject='A new User wants to join your group!', recipients=[owner])
        # message.body = f'User {user_email} wants to join group {group_name} with ID {group_id}. Please log into the Scheduler App to review this request!'
        db.session.add(new_membership)
        db.session.commit()
        # try:
        #     mail.send(message)
        # except Exception as e:
        #     print(f'Error sending request, try again please')
        return redirect(url_for('main.home'))
    # step 3: if step 1 and 2 were completed regularly, close modal, reload home page.
    
@bp.route('/delete_from_group/<int:group_id>', methods=['POST'])
def delete_user_from_group(group_id: int) -> Response :
    """
    Deletes the current user from a specified group

    :group_id: the id of the group to delete the current user from
    """
    # get user email from session
    user_email: str | None = session.get('email')

    # get and validate membership
    membership: Membership = db.session.get(Membership, (user_email, group_id))
    
    if not membership :
        return jsonify(status='error', message='user is not in group'), 401
    
    # delete user and return successful
    db.session.delete(membership)
    db.session.commit()

    return jsonify(status='success'), 201

@bp.route('/change_group_role/<int:group_id>/<string:role>', methods=['POST'])
def change_user_group_role(group_id: int, role: str) -> Response :
    """
    Update a user's role in a group

    :group_id: the id of the group to change the current user's role in
    """
    # get user email from session
    user_email: str | None = session.get('email')

    # get and validate membership
    membership: Membership = db.session.get(Membership, (user_email, group_id))
    
    if not membership :
        return jsonify(status='error', message='user is not in group'), 401
    
    # update membership role
    membership.role = role
    db.session.commit()

    # return success
    return jsonify(status='success'), 201
    

@bp.route('/delete-group/<int:group_id>', methods=['DELETE'])
def delete_group(group_id: int) -> Response:
    """
    This method deletes groups. It checks that the group is owned by the active user.
    """
    # Authenticate the user and check if they are the group admin
    user_email: str = session.get('email')
    membership = db.session.query(Membership).filter_by(user_email=user_email, group_id=group_id).first()

    # Check if the user is the owner of the group
    if membership and membership.role == 'owner':

        # Query the group to delete
        group = db.session.get(Group, group_id)
        try:
            # Delete associated teams
            for team in group.teams :
                for event in team.events :
                    db.session.delete(event)
                db.session.delete(team)
            
            # Delete events
            for event in group.events :
                db.session.delete(event)

            # Delete associated memberships
            for membership in group.memberships :
                db.session.delete(membership)

            # Delete the group
            db.session.delete(group)

            # Commit changes to the database
            db.session.commit()
            return jsonify(status='success')

        except Exception as e:
            # Print failure
            print(f"Exception during commit ${str(e)}")
            # Rollback changes to avoid leaving the database in an inconsistent state
            db.session.rollback()  
            return jsonify(status='fail', error='Error during deletion'), 500
    
    # If the user is not the owner, do not delete
    return jsonify(status='fail'), 500