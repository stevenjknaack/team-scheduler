"""
10stars Flask App Backend

:author : Georgia
:author : Tony
:author : Dante
:author : Steven
:author : Kyle
:author : Anwita
"""
from flask import Flask
from flask_mail import Mail
from .blueprints.auth import auth_blueprint
from .blueprints.events import events_blueprint
from .blueprints.groups import groups_blueprint
from .blueprints.profile import profile_blueprint
from .blueprints.teams import teams_blueprint

from .models import configure_flask_sqlalchemy, SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv() # load environment

def create_app() -> Flask:
    """
    Creates a 10stars Flask app

    :returns: a 10stars Flask app
    """
    path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    app: Flask = Flask(__name__, root_path=path)
    app.secret_key = os.getenv('SECRET_KEY')
    
    # initialize database
    app.db = configure_flask_sqlalchemy(app)
    
    # register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(events_blueprint)
    app.register_blueprint(groups_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(teams_blueprint)

    # configure Flask-Mail API
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USE_SSL'] = False
    # app.config['MAIL_USERNAME'] = '10stars.scheduling@gmail.com'
    # app.config['MAIL_PASSWORD'] = 'ScottDaBeast2023^'
    # app.config['MAIL_DEFAULT_SENDER'] = '10stars.scheduling@gmail.com'

    # mail = Mail(app)

    return app

# create and run app
if __name__ == '__main__':
    app: Flask = create_app()
    app.run(debug=True, port=int(os.getenv('FLASK_PORT')))


