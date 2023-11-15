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
from blueprints.auth import auth_blueprint
from blueprints.events import events_blueprint
from blueprints.groups import groups_blueprint
from blueprints.profile import profile_blueprint
from blueprints.teams import teams_blueprint

from models import *
import os
from dotenv import load_dotenv

load_dotenv()

def create_app() -> Flask:
    app: Flask = Flask(__name__, root_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    app.secret_key: str = os.getenv('SECRET_KEY')
    
    # Initialize Database
    app.db: SQLAlchemy =\
            configure_flask_sqlalchemy(app)
    
    # Register Blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(events_blueprint)
    app.register_blueprint(groups_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(teams_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=os.getenv('FLASK_PORT'))


