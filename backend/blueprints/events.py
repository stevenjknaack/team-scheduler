""" Defines routes for the events """

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, Response, current_app
from models import *
from typing import List, Tuple
from sqlalchemy import text

events_blueprint: Blueprint = Blueprint('events', __name__, 
                                        template_folder='../../templates', 
                                        static_folder='../../static')

@events_blueprint.route('/create-event', methods=['GET'])
def create_event() -> str | Response :

    if 'username' not in session :
        return redirect(url_for(''))
    event_type = request.args.get('type', 'group')
    return render_template('create_event.html', username=session['username'], event_type=event_type)

@events_blueprint.route('/create-event-request', methods=['POST'])
def create_event_request() -> Response :
    """
    This method collects the data inputed by the creator of an event and inserts the information
    into the database. It works by getting the values, creating a connection to the database,
    making a query with the collected values to the database, and once all is done it closes 
    the connection to the database and returns to the profile page

    :author: Dante Katz Andrade
    :version: 2023.10.19
    """
    # Get event data from the HTML form 
    event_type = request.args.get('type', 'group')

    event_name: str = request.form.get('event_name')
    event_description: str = request.form.get('event_description')
    start_day: int = request.form.get('start_day')
    start_month: str = request.form.get('start_month')
    start_year: int = request.form.get('start_year')
    end_day: int = request.form.get('end_day')
    end_month: str = request.form.get('end_month')
    end_year: int = request.form.get('end_year')
    
    # Combine the date components into a single string. Will eventually add time customization 
    start_date = f"{start_year}-{start_month}-{start_day}"
    end_date = f"{end_year}-{end_month}-{end_day}"
    start_time = "9:00:00"
    end_time = "21:00:00"

    # Retrieve user's email 
    user_email: str = session.get('email')
    if user_email:
        db_session = current_app.db.session
        
        
        # Retrieve group_id
        group_query = text("SELECT group_id FROM in_group WHERE user_email = :user_email")
        group_result = db_session.execute(group_query, {'user_email': user_email}).fetchone()


        if group_result is None:
            # No existing group_id, perform insert without group_id
            group_id = None
        else:
            # Extract group_id from group_result
            group_id = group_result[0]

        if event_type == 'group':
            team_id = None
        elif event_type == 'team':
            # Retrieve team_id
            team_query = text("SELECT team_id FROM in_team WHERE user_email = :user_email")
            team_result = db_session.execute(team_query, {'user_email': user_email}).fetchone()
        
            if team_result is None:
                # No existing team_id, perform insert without team_id
                team_id = None
            else:
                # Extract team_id from team_result
                team_id = team_result[0]

        edit_permission = 'group_admin'

        # Create and add the Event to the session
        new_event = Event(
            name=event_name,
            description=event_description,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            edit_permission=edit_permission,
            group_id=group_id,
            team_id=team_id
        )
        db_session.add(new_event)

        # Commit the changes to the database
        db_session.commit()

        # Redirect to the profile page
        return redirect(url_for('auth.home'))

    else:
        # If the user is not logged in, redirect to the login.
        return redirect(url_for('auth.login'))


@events_blueprint.route('/delete-event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id: int) -> Response:
    """
    This method deletes events. It checks that the event is owned by the active user (created by them)
    and then proceeds to execute the query command to delete the event selected.
    """
    db = None
    cursor = db.cursor()

    # Get the owner_id of the event 
    cursor.execute("SELECT edit_permission FROM saved_event WHERE event_id = %s", (event_id,))
    owner = cursor.fetchone()
    
    # Should not be able to delete if button isn't present, which it wouldn't be if there is no event
    # to delete, hoowever as discussed too much security is never bad.
    if owner is None:
        cursor.close()
        db.close()
        return jsonify(status='error', message='Event not found'), 404

    owner_id = owner[0]

    # Check if the user is the owner of the event 
    if 'username' in session:
        cursor.execute("SELECT username FROM user WHERE username = %s", (session['username'],))
        user = cursor.fetchone()
        if user is not None:
            user_id = user[0]
            if user_id == owner_id:
                # Delete the event if user_id matches owner_id and close database 
                cursor.execute("DELETE FROM saved_event WHERE event_id = %s", (event_id,))
                db.commit()
                cursor.close()
                db.close()
                return jsonify(status='success')
            
    # Close database in case of getting around the above if statements. 
    cursor.close()
    db.close()
    return jsonify(status='fail')

@events_blueprint.route('/get-event/<int:event_id>', methods=['GET'])
def get_event(event_id: int) -> Response:
    """
    This method works in tandem with get_user_events. It is called in the JS code after the profile page 
    calls get_user_events and gets all the event id's back. This method then uses the event ID's provided
    to get all the information from each event to display in the profile page.
    """
    db = None
    cursor = db.cursor()

    # Fetch event details using event_id 
    cursor.execute("SELECT * FROM saved_event WHERE event_id = %s", (event_id,))
    event = cursor.fetchone()

    cursor.close()
    db.close()

    if event:
        # return event details as a json object. Format the date as a string if it's a date object
        event_details = {
            "event_name": event[1],
            "start_date": event[2].strftime('%Y-%m-%d'),  
            "end_date": event[3].strftime('%Y-%m-%d'),
            "event_description": event[6]
        }
        return jsonify(event_details)
    else:
        return jsonify(status='error', message='Event not found'), 404

@events_blueprint.route('/get-user-event/<int:event_id>', methods=['GET'])
def get_user_events(username: str) -> List[Tuple]:
    """ Get the events associated with a user """
    # Initiate a connection to the database.
    db = None
    cursor = db.cursor()

    # Fetch user ID by username  
    cursor.execute("SELECT user_id FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()

    # Security check so that people cannot go into the user page without logging in. It may be 
    # redundant with the security check in /profile, however too much security is not a bad thing.
    if user is None:
        cursor.close()
        db.close()
        return [] 

    # Fetch events owned by the user 
    user_id = user[0]
    cursor.execute("SELECT * FROM saved_event WHERE owner_id = %s", (user_id,))
    events = cursor.fetchall()

    # Close connection to database and return all the fetched events.
    cursor.close()
    db.close()

    return events

def add_participant_to_event(event_id: int, user_id: int) -> bool :
    """ Add a participant to an event"""
    # Connect to the database
    db = None
    cursor = db.cursor()

    try:
        # Insert the participant into the event in the database
        query = "INSERT INTO event_participants (event_id, user_id) VALUES (%s, %s)"
        values = (event_id, user_id)
        cursor.execute(query, values)
        db.commit()  # Commit the changes to the database

        return True  # Return True if the participant is added successfully
    except Exception as e:
        # Handle any potential errors, such as database connection issues or constraints
        print(f"Error adding participant to event: {str(e)}")
        db.rollback()  # Rollback the transaction in case of an error
        return False  # Return False to indicate that adding the participant failed
    finally:
        cursor.close()
        db.close()


