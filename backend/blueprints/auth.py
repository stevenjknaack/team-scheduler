from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import bcrypt
from db import get_db

auth_blueprint = Blueprint('auth', __name__, template_folder='../../templates', static_folder='../../static')

@auth_blueprint.route('/')
def index():
    """Home page"""
    if 'username' in session :
        return redirect(url_for('home'))
    return redirect(url_for('auth.login'))

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Render the login form template
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # get data associated with user from database # change the comments
        db = get_db()
        cursor = db.cursor()

        # Use parameterized query
        query = "SELECT * FROM user WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        cursor.close()
        db.close()
        # Check if user exists
    
        if user: # also encry on the frontend
            stored_hashed_password = user[2]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                session['username'] = user[1]
                session['user_id'] = user[0]
                return jsonify(status='success')
            else:
                return jsonify(status='error'), 401
        else:
            return jsonify(status='error', message='Username not found'), 401

""" 
Gets events onwned by user (see get_user_events method) and returns to JS, which then executes
get_event to get the information from each event to display.
"""
@auth_blueprint.route('/profile') # check later
def profile():
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    events = get_db()
    return render_template('profile.html', username=username, events=events)


"""
Gets groups and events owned by user (use get_user_events and get_user_groups) and return to JS, which then executes
"""
@auth_blueprint.route('/home')
def home() :

    return render_template('home.html')

@auth_blueprint.route('/newprofile')
def newprofile() :
    return render_template('newprofile.html')

@auth_blueprint.route('/signup')
def signup() :
    if 'username' in session :
        return redirect(url_for('profile'))
    return render_template('signup.html')

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('index'))

@auth_blueprint.route('/signup-request',  methods=['POST'])
def signup_request():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    # connect to the database
    db = get_db()

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

