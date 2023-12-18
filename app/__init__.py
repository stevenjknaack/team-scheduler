"""
10stars Flask App 

:author : Georgia
:author : Tony
:author : Dante
:author : Steven
:author : Kyle
:author : Anwita
"""
from flask import Flask

from ..config import Config

from .auth.routes import auth_blueprint
from .events.routes import events_blueprint
from .groups.routes import groups_blueprint
from .profile.routes import profile_blueprint
from .teams.routes import teams_blueprint
from .extensions import db, mail

import os

def create_app(config_class=Config) -> Flask:
    """
    Creates a 10stars Flask app 

    :returns: a 10stars Flask app
    """
    # instantiate and configure app
    path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    app: Flask = Flask(__name__, root_path=path)
    app.config.from_object(config_class)

    # initialize the extensions with app
    db.init_app(app)
    mail.init_app(app)
    
    # register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(events_blueprint)
    app.register_blueprint(groups_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(teams_blueprint)

    return app


