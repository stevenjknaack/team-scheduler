# Team Scheduler

# installing virtual environment (recommended) for windows, may need --user flag 
py -m pip install --user virtualenv

# create new venv environment
python -m venv venv

# starting venv in powershell/visual studio terminal (windows)
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\Activate.ps1 

# install Flask
pip install -U Flask
pip install flask flask-cors

# helps run frontend code (not necessary with visual studio code live server)
npm install -g npm
npm install --global http-server

# download python SQL Connector
python -m pip install mysql-connector-python 

# setup
 0. open terminal in vs code
 1. navigate to backend folder and create/activate venv
 2. install flask, http-server, python connector

# to start app
 0. open local terminal, login "ssh -L localhost:23306:localhost:23306 <username>@cs506-team-10.cs.wisc.edu"
 1. open visual studio terminal
 2. navigate to backend folder
 3. activate venv if not active
 3.5. fill in the password,port fields of app.py with steven's mysql password/port
 4. type 'py app.py' to launch backend
 5. right click on index.html and click live server