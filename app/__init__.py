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

from config import Config

from .main import bp as main_bp
from .auth import bp as auth_bp
from .events import bp as events_bp
from .groups import bp as groups_bp
from .profile import bp as profile_bp
from .teams import bp as teams_bp

from .extensions import db, mail

import os

def create_app(config_class=Config) -> Flask:
    """
    Creates a 10stars Flask app 

    :returns: a 10stars Flask app
    """
    # instantiate and configure app
    app: Flask = Flask(__name__)
    app.config.from_object(config_class)

    # initialize extensions with app
    db.init_app(app)
    mail.init_app(app)
    
    # register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(groups_bp, url_prefix='/groups')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(teams_bp, url_prefix='/teams')

    return app


