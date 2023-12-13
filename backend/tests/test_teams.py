""" Test routes and functions of teams.py """
import pytest
from flask import url_for
from flask.testing import FlaskClient
from unittest.mock import patch
import sys
sys.path.append('./backend')
from ..app import create_app
from ..blueprints.teams import teams_blueprint # import obj rather than module
import tempfile
from flask.sessions import SecureCookieSessionInterface
import json

# Setup the Flask test client
@pytest.fixture
def test_client() -> None:
    app = create_app()
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost:6969'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'

    with app.test_client() as client:
        with app.app_context():
            yield app.test_client()