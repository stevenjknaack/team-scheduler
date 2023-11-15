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

    return redirect(url_for('home'))