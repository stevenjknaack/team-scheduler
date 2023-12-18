import pytest
from flask import url_for
from flask.testing import FlaskClient
from unittest.mock import patch
import sys
sys.path.append('./backend')
from .. import create_app
from ..events.routes import events_blueprint # import obj rather than module
import tempfile
from flask.sessions import SecureCookieSessionInterface
import json

# Setup the Flask test client
@pytest.fixture
def test_client() -> None :
    app = create_app()
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost:6969'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'

    with app.test_client() as client:
        with app.app_context():
            yield app.test_client()

@pytest.mark.pytests
def test_create_event_get(test_client: FlaskClient) -> None:
        # Mock the session
        with test_client.session_transaction() as sess:
            sess['username'] = 'testuser'

        # Send a GET request to the route
        response = test_client.get('/create-event/1')

        # Assert the response
        assert response.status_code == 200
        assert 'create_event' in response.data.decode() 

@pytest.mark.pytests
def test_create_event_request_post(test_client: FlaskClient) -> None:
    with test_client as client:
        # Mock the session
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
            sess['email'] = 'testuser@example.com'

        # Prepare mock data for the POST request
        data = {
            'event_name': 'Test Event',
            'event_description': 'Description of Test Event',
            'start_day': '01',
            'start_month': '01',
            'start_year': '2023',
            'end_day': '02',
            'end_month': '01',
            'end_year': '2023',
            'start_time': '08:00',
            'end_time': '17:00',
        }

        # Send a POST request to the route
        response = client.post('/create-event-request/1', data=data)

        # Assert the response
        assert response.status_code == 302  
        assert url_for('auth.home') in response.location



