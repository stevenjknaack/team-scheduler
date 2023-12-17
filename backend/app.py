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

from .config import Config

from .blueprints.auth import auth_blueprint
from .blueprints.events import events_blueprint
from .blueprints.groups import groups_blueprint
from .blueprints.profile import profile_blueprint
from .blueprints.teams import teams_blueprint
from .extensions import db, mail

import os
from dotenv import load_dotenv

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

# create and run app
if __name__ == '__main__':
    app: Flask = create_app()
    app.run(port=int(os.getenv('FLASK_PORT')))


