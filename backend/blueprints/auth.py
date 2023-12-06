""" Defines routes for user authentication """

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, Response, current_app
import bcrypt
from models import *

auth_blueprint: Blueprint = Blueprint('auth', __name__, 
                                      template_folder='../../templates', 
                                      static_folder='../../static')

#db: SQLAlchemy = current_app.db

@auth_blueprint.route('/')
def index() -> Response:
    """
    Home page

    Currently redirects to 
        -login page if not logged in
        -user home page if logged in

    :returns: Redirecting Response
    """
    if 'username' in session :
        return redirect(url_for('auth.home'))
    return redirect(url_for('auth.login'))

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    """
    GET:
        render the login page
    :returns: template-rendering str

    POST:
        submit a login request
    :returns: Response object specifing if successful login or not
    """
    if request.method == 'GET':
        # Render the login form template if not logged in
        if 'username' in session :
            return redirect(url_for('auth.home'))
        return render_template('login.html')
    elif request.method == 'POST':
        email: str = request.form.get('email')
        password: str = request.form.get('password')

        # get user from database 
        user: User = current_app.db.session.get(User, email)

        # Check if user's password is correct
        if user: # also encry on the frontend
            stored_hashed_password: str = user.password
            if bcrypt.checkpw(password.encode('utf-8'),
                            stored_hashed_password.encode('utf-8')):
                session['email'] = user.email
                session['username'] = user.email
                return jsonify(status='success')
            else:
                return jsonify(status='error',  message='Incorrect email or password'), 401
        else:
            return jsonify(status='error', message='Username not found'), 401


@auth_blueprint.route('/profile') 
def profile() -> str | Response:
    """ 
    Gets events onwned by user (see get_user_events method) and returns to JS, which then executes
    get_event to get the information from each event to display.
    """
    if 'username' not in session:
        return redirect(url_for('auth.index'))
    username: str = session['username']
    events = None
    return render_template('profile.html', username=username, events=events)

@auth_blueprint.route('/home')
def home() -> Response:
    """
    Gets groups and events owned by user (use get_user_events and get_user_groups) 
    and return to JS, which then executes
    """
    if 'username' not in session:
        return redirect(url_for('auth.index'))
    email: str = session.get('email')
    
    # Use the SQLAlchemy query attribute for Membership

    user_memberships = current_app.db.session.scalars(current_app.db.select(Membership).filter_by(user_email=email))
    if user_memberships:
        user_groups = [membership.group for membership in user_memberships]
        # initiate list of events to render in home.html
        user_events=[]
        # Loop through groups, and get each event to display in the home page
        for group in user_groups:
            group_id = group.id
            user_events_result = current_app.db.session.scalars(current_app.db.select(Event).filter_by(group_id = group_id))

            for event in user_events_result:
                # Only append valid events, no null events
                if event:
                    user_events.append(event)
        # Render home.html with username from session, groups and events the user participates in.
        return render_template('home.html', username=session.get('username'), user_groups=user_groups, user_events=user_events)
    else: 
        return render_template('home.html', username=session['username'])
    



@auth_blueprint.route('/signup')
def signup() -> str | Response :
    """
    Renders the signup.html page
        or redirects to user home if logged in
    """
    if 'username' in session :
        return redirect(url_for('auth.home'))
    return render_template('signup.html')

@auth_blueprint.route('/logout', methods=['POST'])
def logout() -> Response :
    """
    Logs user out by removing data from session
        and redirecting to the launch page
    """
    if 'username' in session:
        session.pop('username', None)
        session.pop('email', None)
    return redirect(url_for('auth.index'))

@auth_blueprint.route('/signup-request',  methods=['POST'])
def signup_request() -> Response:
    """
    Processes a signup request from the signup page

    :return: Response object with status='success' if 
        successful signup or status='error' if failed
    """
    email: str = request.form.get('email')
    username: str = request.form.get('username')
    password: str = request.form.get('password')

    # check if user already exists
    if current_app.db.session.get(User, email) :
        return jsonify(status='error',  
                    message='An account is already associated with the provided email')

    # hashed_password  # make sure also encry at the frontend
    hashed_password: bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # create a User object
    new_user: User = User(email, username, hashed_password)

    # add new_user to db
    current_app.db.session.add(new_user)
    current_app.db.session.commit()

    # notify success
    return jsonify(status='success')


