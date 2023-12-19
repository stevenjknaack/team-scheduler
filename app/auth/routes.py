""" Defines routes for user authentication """

from flask import render_template, request, redirect, url_for, session, jsonify, Response
import bcrypt
from ..extensions import db
from ..models.user import User
from typing import Union
from ..auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login() -> Union[str , Response]:
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
            return redirect(url_for('main.home'))
        return render_template('login.html')
    elif request.method == 'POST':
        email: str = request.form.get('email')
        password: str = request.form.get('password')

        # get user from database 
        user: User = db.session.get(User, email)

        # Check if user's password is correct
        if user: # also encry on the frontend
            stored_hashed_password: str = user.password
            if bcrypt.checkpw(password.encode('utf-8'),
                            stored_hashed_password.encode('utf-8')):
                session['email'] = user.email
                session['username'] = user.username
                return jsonify(status='success'), 200
            else:
                return jsonify(status='error',  message='Incorrect email or password'), 401
        else:
            return jsonify(status='error', message='Username not found'), 401


    
@bp.route('/signup')
def signup() -> str | Response :
    """
    Renders the signup.html page
        or redirects to user home if logged in
    """
    if 'username' in session :
        return redirect(url_for('main.home'))
    return render_template('signup.html')

@bp.route('/logout', methods=['POST'])
def logout() -> Response :
    """
    Logs user out by removing data from session
        and redirecting to the launch page
    """
    if 'username' in session:
        session.pop('username', None)
        session.pop('email', None)
    return redirect(url_for('main.index'))

@bp.route('/signup-request',  methods=['POST'])
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
    if db.session.get(User, email) :
        return jsonify(status='error',  
                    message='An account is already associated with the provided email'), 412

    # hashed_password  # TODO make sure also encry at the frontend
    hashed_password: bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # create a User object
    new_user: User = User(email, username, hashed_password)

    # add new_user to db
    db.session.add(new_user)
    db.session.commit()

    # notify success
    return jsonify(status='success'), 201



