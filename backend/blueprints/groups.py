from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db import get_db

groups_blueprint = Blueprint('groups', __name__, template_folder='../../templates', static_folder='../../static')
@groups_blueprint.route('/create_group', methods=['POST'])
def create_group():
    """ 
    This method will be made for creating groups. It'll allow for someone to make a group such as 
    CS506Fall23. It will get information such as group name and description. An SQL query will be
    executed to save the group to the database, and then once done it will redirect to home page.
    """
    # Step1: get information from the user such as event name and description.
    # Step2: establish connection to the database and execute the query.
    # Step3: close the database and redirect to home page. 
    
    group_name = request.form.get('group_name')
    group_description = request.form.get('group_description')

    user_id = session.get('user_id')
  
    db = get_db_connection()
    cursor = db.cursor()

    
    query = "INSERT INTO group (group_name, group_description) VALUES (%s, %s);"
    values = (group_name, group_description)
    cursor.execute(query, values)

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('profile'))

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
