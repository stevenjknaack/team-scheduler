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
    return flask.Response(response=json.dumps(return_data), status=201)

# runs connection to frontend
if __name__ == "__main__":
    app.run("localhost", 6969)
