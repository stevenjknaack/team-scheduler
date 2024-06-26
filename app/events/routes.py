""" Defines routes for the events """

from flask import render_template, request, redirect, url_for, session, jsonify, Response
from ..extensions import db
from ..models.membership import Membership
from ..models.event import Event
from datetime import datetime
from ..events import bp
from ..auth.decorators import login_required

@bp.route('/create-event/<int:group_id>', methods=['POST'])
@login_required
def create_event(group_id: int) -> Response :
    """
    This method collects the data inputed by the creator of an event and inserts the information
    into the database. It works by getting the values, creating a connection to the database,
    making a query with the collected values to the database, and once all is done it closes 
    the connection to the database and returns to the profile page

    :author: Dante Katz Andrade
    :version: 2023.10.19
    """
    #from ..blueprints.groups import is_group_admin
    # Get event data from the HTML form 
    event_type = request.args.get('type', 'group')

    event_name: str = request.form.get('event_name') or 'Unnamed Group'
    event_description: str = request.form.get('event_description') or 'No description'
    start_date: str | None = request.form.get('start_date') # Updated
    end_date: str | None = request.form.get('end_date')  # Updated
    reg_start_day: str | None = request.form.get('eventStartDay') 
    reg_end_day: str | None = request.form.get('eventEndDay') 
    start_time: str | None = request.form.get('start_time') 
    end_time: str | None = request.form.get('end_time') 

    # Retrieve user's email 
    user_email: str | None = session.get('email') 
    
    if event_type == 'group':
        team_id = None
    membership = db.session.query(Membership).filter_by(user_email=user_email, group_id=group_id).first()

    if membership and membership.role == 'owner':
        edit_permission = 'group_admin'
    else:
        return redirect(url_for('main.home'))
    
    # update reg_start_day and reg_end_day to be None if invalid
    if not reg_start_day or not reg_end_day :
        reg_start_day = None
        reg_end_day = None

    # Create and add the Event to the session
    new_event = Event(
        name=event_name,
        description=event_description,
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date(), 
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
        reg_start_day = reg_start_day,
        reg_end_day = reg_end_day, 
        start_time=datetime.strptime(start_time, '%H:%M').time(),
        end_time=datetime.strptime(end_time, '%H:%M').time(),
        edit_permission=edit_permission,
        group_id=group_id,
        team_id=team_id
    )
    db.session.add(new_event)

    # Commit the changes to the database
    db.session.commit()

    # Redirect back to page
    return redirect(url_for('groups.group_page', group_id=group_id))


@bp.route('/delete-event/<int:event_id>/<int:group_id>', methods=['DELETE']) #TODO this method should not require group_id
@login_required
def delete_event(event_id: int, group_id: int) -> Response:
    """
    This method deletes events. It checks that the event is owned by the active user (created by them)
    and then proceeds to execute the query command to delete the event selected.
    """
    # Authenticate the user and check if they are the group admin
    user_email: str = session.get('email')

    membership = db.session.query(Membership).filter_by(user_email=user_email, group_id=group_id).first()

    # Check if the user is the owner of the event 
    if not (membership and membership.role == 'owner') :
        # If user is not owner, do not delete.
        return jsonify(status='fail')
    
    # Query the event to delete
    event = db.session.get(Event, event_id)
    # Delete and commit change to db
    db.session.delete(event)
    db.session.commit()
    return jsonify(status='success')
        
    


