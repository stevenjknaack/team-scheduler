# Team Scheduler

# setup (see below for help)
 0. open terminal in vs code
 1. create/activate venv (DO NOT PUSH venv FOLDER TO GIT)
 2. install flask related modules, cryptographic dependencies, environmental variables, and mypy

# to start app
 0. open local terminal, login "ssh -L `<host>`:`<port>`:`<host>`:`<port>` `<username>`@`<cs_address>`"
 1. open visual studio terminal
 2. activate venv if not active
 3. ensure .env is in team-scheduler folder (DO NOT PUSH THIS TO GIT)
 4. use 'py backend/app.py' to launch backend (or with python3: python3 backend/app.py)
 5. open up "localhost:`<flask_port>`" in a browser

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

# install Flask related modules (in venv)
  pip install -U Flask
  pip install flask flask-cors
  pip install -U Flask-SQLAlchemy

# install cryptographic dependencies (in venv)
  pip install pyopenssl
  pip install bcrypt

# install environmental variables (in venv)
  pip install python-dotenv

# install mypy
  pip install mypy

# helpful links
  - our documentation:
      https://docs.google.com/document/d/1_WsgEIjBhdkJ2me_Bu8Fjdv6UBOZOUNW/edit (standards)
      https://docs.google.com/document/d/1mabdPAdAYkwTHhWAPKwwtpW1em9ZWwXFY0fU4rzcjpQ/edit?usp=sharing (recs/specs)
  - flask help:
      https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world (flask megatutorial)
  - flask-sqlalchemy help: 
      https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/ (quick start)
      https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html# (ORM basics)
      https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html (querying with ORM)
  - typing hinting/mpy help:
      https://mypy.readthedocs.io/en/stable/index.html (mypy)
      https://docs.python.org/3/library/typing.html (typing)
      https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html (typing cheat sheat)
  - venv help:
      https://python.land/virtual-environments/virtualenv
  - unit testing in python/flask
      https://realpython.com/python-testing/#testing-for-web-frameworks-like-django-and-flask
