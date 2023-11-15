""" Defines group related routes """

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, Response, current_app
from models import *

groups_blueprint = Blueprint('groups', __name__, 
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

def is_group_admin(group_id, user_id):
    # Connect to the database
    db = get_db_connection()
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

def get_group_members(group_id):
    # Connect to the database
    db = get_db_connection()
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
