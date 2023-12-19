""" Defines routes for user authentication """

from flask import render_template, redirect, url_for, session, jsonify, Response
from ..extensions import db
from ..models.user import User
from ..models.membership import Membership
from ..models.event import Event
from ..models.group import Group
from typing import List
from app.main import bp

@bp.route('/')
def index() -> Response:
    """
    Home page

    Currently redirects to 
        -login page if not logged in
        -user home page if logged in

    :returns: Redirecting Response
    """
    if 'username' in session :
        return redirect(url_for('main.home'))
    return redirect(url_for('auth.login'))

@bp.route('/home')
def home() -> Response:
    """
    Gets groups and events owned by user (use get_user_events and get_user_groups) 
    and return to JS, which then executes
    """
    if 'username' not in session:
        return redirect(url_for('main.index'))
    email: str = session.get('email')
    
    # Use the SQLAlchemy query attribute for Membership

    user_memberships = db.session.scalars(db.select(Membership).filter_by(user_email=email))
    if user_memberships:
        user_groups = [membership.group for membership in user_memberships]
        # initiate list of events to render in home.html
        user_events=[]
        # Loop through groups, and get each event to display in the home page
        for group in user_groups:
            group_id = group.id
            user_events_result = db.session.scalars(db.select(Event).filter_by(group_id = group_id))

            for event in user_events_result:
                # Only append valid events, no null events
                if event:
                    user_events.append(event)
        # Render home.html with username from session, groups and events the user participates in.
        return render_template('home.html', username=session.get('username'), user_groups=user_groups, user_events=user_events)
    else: 
        return render_template('home.html', username=session['username'])

@bp.route('/get-notifications',  methods=['GET'])
def get_user_notifications() -> Response :
    """ 
    Returns all the notifications associated with the current user.
    Currently, just returns the group invites
    """
    # get the user's email from session
    user_email: str | None = session.get('email')

    # check if user_email exists
    if not user_email :
        return jsonify(status='failure'), 500
    
    # get and validate user
    user: User | None = db.session.get(User, user_email)

    if not user :
        return jsonify(status='failure'), 500

    # get users group invites
    inviting_groups: List[Group] = user.get_group_invites()
    print(inviting_groups)
    # return
    return jsonify([{'id': group.id, 'name': group.name} for group in inviting_groups]), 200




