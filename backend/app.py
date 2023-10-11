from flask import Flask, request
import flask
import json
from flask_cors import CORS
import mysql.connector
import secrets

# database connection
mydb = mysql.connector.connect(
  host = "localhost",
  port = secrets.port,
  user = "root",
  password = secrets.password,
  database = "10stars"
)

print('established connection to database...')

# recieve and send to frontend
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "success"

# function for dealing with request from front end for user data
@app.route('/users', methods=["POST"])
def users():
    # get data (username) from front end
    print("users endpoint reached...")
    received_data = request.get_json()
    print(f"received data: {received_data}")
    message = received_data['data']

    # get data associated with user from database
    mycursor = mydb.cursor()
    mycursor.execute(f'select * from user where username = "{message}"')
    myresult = mycursor.fetchall()
    
    return_userdata = 'no data registered'
    if len(myresult) > 0 :
        return_userdata = myresult[0][1]

    # return data retrieved from database
    return_data = {
        "status": "success",
        "message": f"{return_userdata}"
    }
    return flask.Response(response=json.dumps(return_data), status=201) #201 for post return, 200 for get

@app.route('/login', methods=['POST'])
def login():
    received_data = request.get_json()
    print(f"received data: {received_data}")
    email = received_data['email']
    password = received_data['password']

    # get data associated with user from database
    mycursor = mydb.cursor()
    mycursor.execute(f'select * from user where username = "{email}"')
    user = mycursor.fetchone()
    print('this is user', user)
    print('this is user password', user[1])
    mycursor.close()
    if not user:
        print('no user')
        return flask.jsonify({'status': 'error', 'message': 'User not found'}), 401

    if user[1] != password:  # IMPORTANT: This is a simple example. In a real app, passwords should be hashed!
        print('incorrect password')
        return flask.jsonify({'status': 'error', 'message': 'Invalid password'}), 401

    # Login successful, handle the session or return a success message
    print('correct password')
    return flask.jsonify({'status': 'success', 'message': 'Logged in successfully'})

# runs connection server to frontend
if __name__ == "__main__":
    app.run("localhost", 6969)
