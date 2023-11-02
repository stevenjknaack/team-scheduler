"""
10stars Flask App Backend

:author : Georgia
:author : Tony
:author : Dante
:author : Steven
:author : Kyle
:author : Anwita
"""
# conisdering combining all the similar query behavior

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv() # add variables to the environment

app = Flask(__name__, root_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CORS(app)
app.secret_key = os.getenv('DB_PASSWORD') # redundant with line31

def get_db_connection():
    """Returns connection object to database"""
    return mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        port = os.getenv('DB_PORT'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME')
    )

@app.route('/')
def index():
    """Home page"""
    if 'username' in session :
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET']) # redundant with above
def login():
    if 'username' in session :
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/login-request', methods=['POST'])
def login_request():
    # post 
    email = request.form.get('email')
    password = request.form.get('password')

    # get data associated with user from database # change the comments
    db = get_db_connection() 
    cursor = db.cursor()

    # Use parameterized query
    query = "SELECT * FROM user WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    db.close()
    # Check if user exists
    
    if user: # also encry on the frontend
        stored_hashed_password = user[3]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            session['username'] = user[2]
            session['user_id'] = user[0]
            return jsonify(status='success')
        else:
            return jsonify(status='error'), 401
    else:
        return jsonify(status='error', message='Username not found'), 401

""" 
This function gets all the events created by the active user to display at the profile page.
"""

def get_user_events(username):

    """ Initiate a connection to the database. """

    db = get_db_connection()
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
    
""" 
Gets events onwned by user (see get_user_events method) and returns to JS, which then executes
get_event to get the information from each event to display.
"""
@app.route('/profile') # check later
def profile():
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    events = get_user_events(username)
    return render_template('profile.html', username=username, events=events)


@app.route('/signup')
def signup() :
    if 'username' in session :
        return redirect(url_for('profile'))
    return render_template('signup.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/signup-request',  methods=['POST'])
def signup_request():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    # connect to the database
    db = get_db_connection()

    # create a cursor
    cursor = db.cursor()
    query = "INSERT INTO user (email, username, password) VALUES (%s, %s, %s);"

    # hashed_password  # make sure also encry at the frontend
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    values = (email, username, hashed_password) 

    # use the cursor to execute the query 
    cursor.execute(query, values)

    # commit change to database
    db.commit()  

    # close cursor and database
    cursor.close()
    db.close()
    return jsonify(status='success')

@app.route('/create-event', methods=['GET'])
def create_event():
    if 'username' not in session :
        return redirect(url_for('login'))
    return render_template('create_event.html', username=session['username'])

"""
This method collects the data inputed by the creator of an event and inserts the information
into the database. It works by getting the values, creating a connection to the database,
making a query with the collected values to the database, and once all is done it closes 
the connection to the database and returns to the profile page
@author: Dante Katz Andrade
@version 2023.10.19
"""
@app.route('/create-event-request', methods=['POST'])
def create_event_request():
    """ Get event data from the HTML form """
    event_name = request.form.get('event_name')
    event_description = request.form.get('event_description')
    start_day = request.form.get('start_day')
    start_month = request.form.get('start_month')
    start_year = request.form.get('start_year')
    end_day = request.form.get('end_day')
    end_month = request.form.get('end_month')
    end_year = request.form.get('end_year')
    
    """ Combine the date components into a single string. Will eventually add time customization """
    start_date = f"{start_year}-{start_month}-{start_day}"
    end_date = f"{end_year}-{end_month}-{end_day}"
    start_time = "9:00:00"
    end_time = "21:00:00"

    user_id = session.get('user_id')
  
    """ Connect to the database """
    db = get_db_connection()
    cursor = db.cursor()

    """ Insert the event data into the "savedEvent" table """
    query = "INSERT INTO saved_event (event_name, start_date, end_date, start_time, end_time, event_description, owner_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    values = (event_name, start_date, end_date, start_time, end_time, event_description, user_id)
    cursor.execute(query, values)
    
    """ Commit the changes to the database and close the cursor and database connection. """
    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('profile'))

""" 
This method will be made for creating groups. It'll allow for someone to make a group such as 
CS506Fall23. It will get information such as group name and description. An SQL query will be
executed to save the group to the database, and then once done it will redirect to home page.
"""
@app.route('/create_group', methods=['POST'])
def create_group():
    """
    This part will get information from the user such as event name and description.
    The next step will be to establish connection to the database and execute the query.
    Then we close the database and redirect to home page. 
    """

"""
This method will use an algorithm to generate teams within a group, such as T_1->T_10 part of 
CS50Fall623. It will then send invitations to users to their respective teams which they will be
able to accept or deny. It inserts all the teams generated to the database, and once a user accepts
their invitation they will be put into the database under their team (see accept_invite method).
"""
@app.route('/generate_teams', methods=['POST'])
def generate_teams():
    """ Get list of group participants as well as their time availability from database. """

    """ Insert into algorithm """

    """ Send invite to all users in group to their respective teams """

    """ return succesful Jquery """
"""
This Method will allow for creating a team manually, without needing time availabilty. A user who 
creates a team can give a name to the team and insert people manually into it by providing their email.
Other USers who have been invited will get a notification which will allow them to accept or deny invitation.
"""
@app.route('/manual_create_teams', methods=['POST'])
def create_team():
    """ Creates a team with team name and size. """
    """ Get information from group participant via email from DB"""
    """ Commit team to DB """
    """ Commit participants into DB """
    """ Return succesful JQuery """
@app.route('/send-invitations', methods=['POST'])
def send_invitations():
    # Get JSON data sent from the frontend
    data = request.get_json()

    # Extract email addresses
    emails = data.get('emails', [])

    # placeholder
    event_id = 5

    # connect to database
    db = get_db_connection()

    # create a cursor 
    cursor = db.cursor()

    for email in emails:
        query = "INSERT INTO participates_in (user_email, event_id, user_role) VALUES (%s, %s, %s)"
        values = (email, event_id, 0)
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
This method deletes events. It checks that the event is owned by the active user (created by them)
and then proceeds to execute the query command to delete the event selected.
"""
@app.route('/delete-event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):

    db = get_db_connection()
    cursor = db.cursor()

    """ Get the owner_id of the event """

    cursor.execute("SELECT owner_id FROM saved_event WHERE event_id = %s", (event_id,))
    owner = cursor.fetchone()
    """
    Should not be able to delete if button isn't present, which it wouldn't be if there is no event
    to delete, hoowever as discussed too much security is never bad.
    """
    if owner is None:
        cursor.close()
        db.close()
        return jsonify(status='error', message='Event not found'), 404

    owner_id = owner[0]

    """ Check if the user is the owner of the event """
    if 'username' in session:
        cursor.execute("SELECT user_id FROM user WHERE username = %s", (session['username'],))
        user = cursor.fetchone()
        if user is not None:
            user_id = user[0]
            if user_id == owner_id:

                """ Delete the event if user_id matches owner_id and close database """

                cursor.execute("DELETE FROM saved_event WHERE event_id = %s", (event_id,))
                db.commit()
                cursor.close()
                db.close()
                return jsonify(status='success')
    """ Close database in case of getting around the above if statements. """
    cursor.close()
    db.close()
    return jsonify(status='fail')
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

if __name__ == '__main__':
    app.run(debug = True, port = os.getenv('FLASK_PORT'))  # Running the app on localhost:<PORT>
