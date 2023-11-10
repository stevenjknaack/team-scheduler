from flask import g
from flask import current_app as app
import mysql.connector
import os

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            user = os.getenv('DB_USER'), 
            password = os.getenv('DB_PASSWORD'), 
            host = os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT'), 
            database = os.getenv('DB_NAME')
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)
