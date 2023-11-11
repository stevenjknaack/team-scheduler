"""
10stars Flask App Backend

:author : Georgia
:author : Tony
:author : Dante
:author : Steven
:author : Kyle
:author : Anwita
"""
from flask import Flask
from blueprints.auth import auth_blueprint
from blueprints.events import events_blueprint
from blueprints.teams import teams_blueprint
from blueprints.groups import groups_blueprint
from db import init_db
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__,  root_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    app.secret_key = os.getenv('SECRET_KEY')
    
    # Initialize Database
    init_db(app)

    # Register Blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(events_blueprint)
    app.register_blueprint(groups_blueprint)
    app.register_blueprint(teams_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=os.getenv('FLASK_PORT'))

"""
This method works in tandem with get_user_events. It is called in the JS code after the profile page 
calls get_user_events and gets all the event id's back. This method then uses the event ID's provided
to get all the information from each event to display in the profile page.
"""
@app.route('/get-event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    db = get_db_connection()
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

@app.route('/group/<int:group_id>/create-event', methods=['POST'])
def create_group_event(group_id):
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

def add_participant_to_event(event_id, user_id):
    # Connect to the database
    db = get_db_connection()
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

if __name__ == '__main__':
    app.run(debug = True, port = os.getenv('FLASK_PORT'))  # Running the app on localhost:<PORT>

