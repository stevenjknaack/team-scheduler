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
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    # get 

    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        # post 
        username = request.form.get('username')
        password = request.form.get('password')

        # get data associated with user from database
        db = get_db_connection()
        cursor = db.cursor()

        # Use parameterized query
        query = "SELECT * FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        cursor.close()
        db.close()
        # Check if user exists
        if user:
            if user[1] == password:
                session['username'] = user[0]
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

@app.route('/signup',  methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hash the password
        db = get_db_connection()
        cursor = db.cursor()

        query = "INSERT INTO user (username, data) VALUES (%s, %s);"
        values = (username, password)  # Hashed password is a bytes object; decode it to string
        cursor.execute(query, values)

        db.commit()  # Don't forget to commit your changes

        cursor.close()
        db.close()
        return jsonify(status='success')
        #return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, port=6969)  # Running the app on localhost:6969
