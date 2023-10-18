"""Backend for application"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import mysql.connector
import mysecrets
import bcrypt
import os

app = Flask(__name__, root_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CORS(app)
app.secret_key = 'mysecrets.password' 

def get_db_connection():
    """Returns connection object to database"""
    return mysql.connector.connect(
        host = "localhost",
        port = mysecrets.port,
        user = "root",
        password = mysecrets.password,
        database = "10stars"
    )

@app.route('/')
def index():
    """Home page"""
    if 'username' in session :
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    if 'username' in session :
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/login-request', methods=['POST'])
def login_request():
    # post 
    email = request.form.get('email')
    password = request.form.get('password')

    # get data associated with user from database
    db = get_db_connection()
    cursor = db.cursor()

    # Use parameterized query
    query = "SELECT * FROM user WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    db.close()
    # Check if user exists
    print(user)
    if user:
        stored_hashed_password = user[3]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            session['username'] = user[2]
            return jsonify(status='success')
        else:
            return jsonify(status='error'), 401
    else:
        return jsonify(status='error', message='Username not found'), 401

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('profile.html', username=session['username'])

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

    # Hash the password
    db = get_db_connection()
    cursor = db.cursor()

    query = "INSERT INTO user (email, username, password) VALUES (%s, %s, %s);"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # store hashed_password in the database
    values = (email, username, hashed_password)  # Hashed password is a bytes object; decode it to string
    cursor.execute(query, values)

    db.commit()  # Don't forget to commit your changes

    cursor.close()
    db.close()
    return jsonify(status='success')
    #return render_template('login.html')

@app.route('/create-event', methods=['GET'])
def create_event():
    if 'username' not in session :
        return redirect(url_for('login'))
    return render_template('create_event.html', username=session['username'])

@app.route('/create-event-request', methods=['POST'])
def create_event_request():
    # Get event data from the HTML form
    event_name = request.form.get('event_name')
    event_description = request.form.get('event_description')
    start_day = request.form.get('start_day')
    start_month = request.form.get('start_month')
    start_year = request.form.get('start_year')
    end_day = request.form.get('end_day')
    end_month = request.form.get('end_month')
    end_year = request.form.get('end_year')
    
    # Combine the date components into a single string
    start_date = f"{start_year}-{start_month}-{start_day}"
    end_date = f"{end_year}-{end_month}-{end_day}"
    print("the values are: ", start_date, end_date)
    start_time = "9:00:00"
    end_time = "21:00:00"

    # Connect to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Insert the event data into the "savedEvent" table
    query = "INSERT INTO saved_event (event_name, start_date, end_date, start_time, end_time, event_description) VALUES (%s, %s, %s, %s, %s, %s);"
    values = (event_name, start_date, end_date, start_time, end_time, event_description)
    cursor.execute(query, values)

    # Commit the changes to the database
    db.commit()

    # Close the cursor and the database connection
    cursor.close()
    db.close()

    return redirect(url_for('profile'))


if __name__ == '__main__':
    app.run(debug=True, port=6969)  # Running the app on localhost:6969
