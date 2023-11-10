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
from blueprints.teams import teams_blueprint
from blueprints.groups import groups_blueprint
from db import init_db
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__,  root_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    app.secret_key = os.getenv('SECRET_KEY')
    
    # Initialize Database
    init_db(app)

    # Register Blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(events_blueprint)
    app.register_blueprint(groups_blueprint)
    app.register_blueprint(teams_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=os.getenv('FLASK_PORT'))
