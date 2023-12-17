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
from .blueprints.auth import auth_blueprint
from .blueprints.events import events_blueprint
from .blueprints.groups import groups_blueprint
from .blueprints.profile import profile_blueprint
from .blueprints.teams import teams_blueprint
from .extensions import db, mail

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
    
    # configure the MYSQL database, relative to the app instance
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize the app with the extension
    db.init_app(app)

    # initialize mail with the app
    mail.init_app(app)
    
    # register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(events_blueprint)
    app.register_blueprint(groups_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(teams_blueprint)

    # configure Flask-Mail API
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    # mail = Mail(app)

    return app

# create and run app
if __name__ == '__main__':
    app: Flask = create_app()
    app.run(debug=True, port=int(os.getenv('FLASK_PORT')))


