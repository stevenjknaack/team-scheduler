# Team Scheduler

# setup (see below for help)
 0. open terminal in vs code
 1. navigate to backend folder and create/activate venv (DO NOT PUSH venv FOLDER TO GIT)
 2. install flask, python connector, cryptographic dependencies, and environmental variables

# to start app
 0. open local terminal, login "ssh -L localhost:63306:localhost:63306 <username>@cs506-team-10.cs.wisc.edu"
 1. open visual studio terminal
 2. navigate to backend folder
 3. activate venv if not active
 3.5. ensure .env is in team-scheduler folder (DO NOT PUSH THIS TO GIT)
 4. type 'py app.py' to launch backend (for people using python3: python3 app.py)
 5. open up "localhost:6969" in a browser

# to run the unit testing
  - python -m unittest discover
  - Other possible command: (for people using python3: remove _init_.py) python3 -m unittest my_tests -v (after locating at the test folder)

# installing virtual environment (recommended, not required), may need --user flag 
  py -m pip install --user virtualenv

# create new venv environment (in any subfolder but root is recommended)
  python -m venv venv

# starting venv in windows with powershell/visual studio terminal 
  Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process
  venv\Scripts\Activate.ps1 

# starting venv on mac
  source myvenv/bin/activate

# install Flask (in venv)
  pip install -U Flask
  pip install flask flask-cors

# install python SQL Connector (in venv)
  python -m pip install mysql-connector-python 

# install cryptographic dependencies (in venv)
  pip install pyopenssl
  pip install bcrypt

# install environmental variables (in venv)
  pip install python-dotenv

# if there's an error connecting to the database, it may need to be created again
  0. "ssh <username>@cs506-team-10.cs.wisc.edu" and 
    ensure you're in a directory with 10stars.yml 
  1. run "docker ps" and see if it is up and running, continue if not
  2. create sql server 10stars.yml "docker compose -f 10stars.yml -p 10stars up -d"
  3. connect to it "mysql -h localhost -P 63306 --protocol=TCP -u root -p"
  4. copy and paste contents of db_setup.txt, press enter, should be no errors
  5. quit terminal

# helpful links
  - Standard Document we followed:
      [Standard Document](https://docs.google.com/document/d/1_WsgEIjBhdkJ2me_Bu8Fjdv6UBOZOUNW/edit)
  - frontend-backend flask help: 
      https://tms-dev-blog.com/python-backend-with-javascript-frontend-how-to/#Prerequisites
  - python to mysql help:
      https://www.w3schools.com/nodejs/nodejs_mysql.asp
  - venv help:
      https://python.land/virtual-environments/virtualenv
  - unit testing in python/flask
      https://realpython.com/python-testing/#testing-for-web-frameworks-like-django-and-flask
