# Team Scheduler

# setup (see below for help)
 0. open terminal in vs code
 1. navigate to backend folder and create/activate venv (DO NOT PUSH venv FOLDER TO GIT)
 2. install flask, http-server, python connector

# to start app
 0. open local terminal, login "ssh -L localhost:63306:localhost:63306 <username>@cs506-team-10.cs.wisc.edu"
 1. open visual studio terminal
 2. navigate to backend folder
 3. activate venv if not active
 3.5. ensure secrets.py is in backend folder (DO NOT PUSH THIS TO GIT)
 4. type 'py app.py' to launch backend
 5. right click on index.html and click live server

# installing virtual environment (recommended, not required), may need --user flag 
  py -m pip install --user virtualenv

# create new venv environment (do in backend folder)
  python -m venv venv

# starting venv in windows with powershell/visual studio terminal 
  Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process
  venv\Scripts\Activate.ps1 

# starting venv on mac
  source myvenv/bin/activate

# install Flask (do in venv)
  pip install -U Flask
  pip install flask flask-cors

# helps run frontend code (not necessary with visual studio code live server) (do in venv)
  npm install -g npm
  npm install --global http-server

# download python SQL Connector (do in venv)
  python -m pip install mysql-connector-python 

# if there's an error connecting to the database, it may need to be created again
  0. "ssh <username>@cs506-team-10.cs.wisc.edu" and 
    ensure you're in a directory with 10stars.yml 
  1. run "docker ps" and see if it is up and running, continue if not
  2. create sql server 10stars.yml "docker compose -f 10stars.yml -p 10stars up -d"
  3. connect to it "mysql -h localhost -P 63306 --protocol=TCP -u root -p"
  4. copy and paste contents of db_setup.txt, press enter, should be no errors
  5. quit terminal

# helpful links
  - frontend-backend flask help: 
      https://tms-dev-blog.com/python-backend-with-javascript-frontend-how-to/#Prerequisites
  - python to mysql help:
      https://www.w3schools.com/nodejs/nodejs_mysql.asp
  - venv help:
      https://python.land/virtual-environments/virtualenv