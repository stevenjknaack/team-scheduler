from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

profile_blueprint: Blueprint = Blueprint('profile', __name__, 
                            template_folder='../../templates', static_folder='../../static')

@profile_blueprint.route('/save_schedule', methods=['POST'])
def save_schedule():
    """
    TODO: This Method will allow for saving the availability to the availability table. 
    """

    """ Get Username and avail blocks """
    data = request.get_json()
    username = data['username']
    schedules = data['schedule']

    """ Get connection to database """
    db = get_db_connection()
    cursor = db.cursor()

    """ Check if user had saved availability"""
    cursor.execute("SELECT * FROM your_table_name WHERE user_email LIKE %s", (username,))
    user = cursor.fetchone()    
    if user:
        """ delete all user availability """
        """ insert new availability """
    else:
        """ else, insert avail blocks into table"""
        for schedule in schedules:
            day = schedule['day']
            start_time = schedule['startTime']
            end_time = schedule['endTime']
            query = "INSERT INTO schedule_table (start_day, end_day, start_time, end_time, user_email) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query, (day, day, start_time, end_time, username,))
        db.commit()          
    """ close connection """
    cursor.close()
    db.close()

    """ return succesful Jquery """