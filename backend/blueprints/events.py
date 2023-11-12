from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db import get_db

events_blueprint = Blueprint('events', __name__, template_folder='../../templates', static_folder='../../static')

""" 
This function gets all the events created by the active user to display at the profile page.
"""
@events_blueprint.route('/create-event', methods=['GET'])
def create_event():
    if 'username' not in session :
        return redirect(url_for(''))
    return render_template('create_event.html', username=session['username'])

@events_blueprint.route('/create-event-request', methods=['POST'])
def create_event_request() -> None:
    """
    This method collects the data inputed by the creator of an event and inserts the information
    into the database. It works by getting the values, creating a connection to the database,
    making a query with the collected values to the database, and once all is done it closes 
    the connection to the database and returns to the profile page
    @author: Dante Katz Andrade
    @version 2023.10.19
    """
    # Get event data from the HTML form 
    event_name = request.form.get('event_name')
    event_description = request.form.get('event_description')
    start_day = request.form.get('start_day')
    start_month = request.form.get('start_month')
    start_year = request.form.get('start_year')
    end_day = request.form.get('end_day')
    end_month = request.form.get('end_month')
    end_year = request.form.get('end_year')
    
    # Combine the date components into a single string. Will eventually add time customization 
    start_date = f"{start_year}-{start_month}-{start_day}"
    end_date = f"{end_year}-{end_month}-{end_day}"
    start_time = "9:00:00"
    end_time = "21:00:00"

    # Retrieve user's email 
    user_email = session.get('user_id')

    if user_email:
        db = get_db()
        cursor = db.cursor()

        # Retrieve group_id 
        #cursor.execute("SELECT group_id FROM in_group WHERE user_email = %s", (user_email,))
        #group_id = cursor.fetchone()[0]
        group_id = 10000

        cursor.execute("SELECT team_id FROM in_team WHERE user_email = %s", (user_email,))
        team_result = cursor.fetchone()
        if team_result: 
            team_id = team_result[0]
            edit_permission = 'group_admin'
            # Insert the event data into the "savedEvent" table 
            query = "INSERT INTO event (name, description, start_date, end_date, start_time, end_time, edit_permission, group_id, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            values = (event_name, event_description, start_date, end_date, start_time, end_time, edit_permission, group_id, team_id)
            cursor.execute(query, values)

            # Commit the changes to the database and close the cursor and database connection. 
            db.commit()
            cursor.close()
            db.close()
            return redirect(url_for('profile'))            
        
        else: 
            edit_permission = 'group_admin'
            # Insert the event data into the "savedEvent" table 
            query = "INSERT INTO event (name, description, start_date, end_date, start_time, end_time, edit_permission, group_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            values = (event_name, event_description, start_date, end_date, start_time, end_time, edit_permission, group_id)
            cursor.execute(query, values)

            # Commit the changes to the database and close the cursor and database connection. 
            db.commit()
            cursor.close()
            db.close()
            return redirect(url_for('profile'))            
        
        edit_permission = 'group_admin'
        # Insert the event data into the "savedEvent" table 
        query = "INSERT INTO event (name, description, start_date, end_date, start_time, end_time, edit_permission, group_id, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (event_name, event_description, start_date, end_date, start_time, end_time, edit_permission, group_id, team_id)
        cursor.execute(query, values)

        # Commit the changes to the database and close the cursor and database connection. 
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('profile'))
    else:
        # If the user is not logged in, redirect to the login.
        return redirect(url_for('login'))

@events_blueprint.route('/delete-event/<int:event_id>', methods=['DELETE'])
#def delete_event(event_id: int) -> Union[dict, tuple]:
def delete_event(event_id: int):
    """
    This method deletes events. It checks that the event is owned by the active user (created by them)
    and then proceeds to execute the query command to delete the event selected.
    """

    db = get_db()
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

@events_blueprint.route('/send-invitations', methods=['POST'])
def send_invitations():
    # Get JSON data sent from the frontend
    data = request.get_json()

    # Extract email addresses
    emails = data.get('emails', [])

    
    # placeholder
    event_id = 5

    # connect to database
    db = get_db()

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


"""
This method works in tandem with get_user_events. It is called in the JS code after the profile page 
calls get_user_events and gets all the event id's back. This method then uses the event ID's provided
to get all the information from each event to display in the profile page.
"""
@events_blueprint.route('/get-event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    db = get_db()
    cursor = db.cursor()

    """ Fetch event details using event_id """

    cursor.execute("SELECT * FROM saved_event WHERE event_id = %s", (event_id,))
    event = cursor.fetchone()

    cursor.close()
    db.close()

    if event:

        """ return event details as a json object. Format the date as a string if it's a date object """
        
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
def get_user_events(username):
    """ Initiate a connection to the database. """

    db = get_db()
    cursor = db.cursor()

    """ Fetch user ID by username  """

    cursor.execute("SELECT user_id FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()

    """ Security check so that people cannot go into the user page without logging in. It may be 
    redundant with the security check in /profile, however too much security is not a bad thing."""

    if user is None:
        cursor.close()
        db.close()
        return [] 

    """ Fetch events owned by the user """

    user_id = user[0]
    cursor.execute("SELECT * FROM saved_event WHERE owner_id = %s", (user_id,))
    events = cursor.fetchall()

    """ Close connection to database and return all the fetched events. """

    cursor.close()
    db.close()

    return events
