import pytest
from flask import session, g, url_for
from flask.testing import FlaskClient
import sys
import os
sys.path.append('./backend')
from app import create_app
from ..blueprints.auth import auth_blueprint # import obj rather than module
from unittest.mock import patch
from werkzeug.security import generate_password_hash
from backend.models.models import User 
import time
import bcrypt

# A fixture is where a client is define, we want to simulate requests to the app
@pytest.fixture
def client_and_app() -> None :
    app = create_app()
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost:6969'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'

    with app.test_client() as client:
        with app.app_context():
            yield client, app

# Test the redirection behavior of the index route
@pytest.mark.pytests
def test_index_route(client_and_app: FlaskClient) -> None:
    client, app = client_and_app
    # Simulate a user not in session (commented out)
    response = client.get('/')
    # expect a redirection
    assert response.status_code == 302
    assert url_for('auth.login') in response.location

# Test the login GET request
@pytest.mark.pytests
def test_login_get(client_and_app: FlaskClient) -> None :
    client, app=client_and_app 
    response = client.get(url_for('auth.login'))
    assert response.status_code == 200
    assert b'loginForm' in response.data 

# Test the login POST request
@pytest.mark.pytests
def test_login_post(client_and_app: FlaskClient) -> None :
    client, app = client_and_app

    # Generate unique test data
    unique_suffix = str(int(time.time()))
    test_email = f"testuser{unique_suffix}@example.com"
    test_username = f"testuser{unique_suffix}"
    test_password = "testpass"

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())

    # Ensure the database is in a clean state
    with app.app_context():
        existing_user = app.db.session.execute(
            app.db.select(User).filter_by(email=test_email)
        ).scalar_one_or_none()

        if existing_user:
            app.db.session.delete(existing_user)
            app.db.session.commit()

        # Create a test user in the database
        new_user = User(email=test_email, username=test_username, password=hashed_password)
        app.db.session.add(new_user)
        app.db.session.commit()

    # Attempt to login with the test user credentials
    response = client.post(url_for('auth.login'), data={
        'email': test_email,
        'password': test_password
    })

    assert response.status_code == 200

    # Clean up test data by removing the user
    with app.app_context():
        app.db.session.delete(new_user)
        app.db.session.commit()

# Test the signup GET request
def test_signup_get(client_and_app: FlaskClient) -> None :
    client, app=client_and_app
    response = client.get(url_for('auth.signup'))
    assert response.status_code == 200
    assert b'signupForm' in response.data 

# # Test the signup POST request
#@patch('blueprints.auth.get_db')
@pytest.mark.pytests
def test_signup_post(client_and_app):
    client, app = client_and_app

    # Create test data
    test_email = "newuser@example.com"
    test_username = "newuser"
    test_password = "newpassword"

    # Test signup POST request
    response = client.post(url_for('auth.signup_request'), data={
        'email': test_email,
        'username': test_username,
        'password': test_password
    })

    # Verify response for successful signup
    assert response.status_code == 200

    # Clean up test data
    with app.app_context():
        user = app.db.session.execute(
            app.db.select(User).filter_by(email=test_email)
        ).scalar_one_or_none()
        if user:
            app.db.session.delete(user)
            app.db.session.commit()

    # Test for duplicate signup attempt
    response = client.post(url_for('auth.signup_request'), data={
        'email': test_email,
        'username': test_username,
        'password': test_password
    })

    # Verify response for duplicate signup
    assert response.status_code == 200  

# # Test the logout
@pytest.mark.pytests
def test_logout(client_and_app: FlaskClient) -> None :
    client, app = client_and_app
    # simualte a "POST" request to logout route
    response = client.post(url_for('auth.logout'))
    assert response.status_code == 302
    assert url_for('auth.index') in response.location
