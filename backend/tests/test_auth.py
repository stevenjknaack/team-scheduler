""" Test routes and functions of auth.py """

import pytest
from flask import session, g, url_for, FlaskClient
from unittest.mock import patch
from werkzeug.security import generate_password_hash
from blueprints.auth import auth_blueprint
# Assuming auth.py is in the same directory as this test file

@pytest.fixture
def client() -> None :
    """ Setup the Flask test client """
    app = create_app()
    app.register_blueprint(auth_blueprint)
    with app.test_client() as client:
        yield client

def test_index_route(client: FlaskClient) -> None :
    """ Test the redirection behavior of the index route """
    with client:
        # Simulate a user not in session
        response = client.get('/')
        assert response.status_code == 302
        assert url_for('auth.login') in response.location

        # Simulate a user in session
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
        response = client.get('/')
        assert response.status_code == 302
        assert url_for('profile') in response.location

def test_login_get(client: FlaskClient) -> None :
    """ Test the login GET request """
    response = client.get(url_for('auth.login'))
    assert response.status_code == 200
    assert b'login.html' in response.data

@patch('auth.get_db')
def test_login_post(mock_get_db, client: FlaskClient) -> None:
    """ Test the login POST request """
    mock_cursor = mock_get_db.return_value.cursor.return_value
    mock_cursor.execute.return_value = None
    mock_cursor.fetchone.return_value = {
        'id': 1, 'username': 'testuser', 'password': generate_password_hash('testpass')
    }
    
    response = client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    
    with client.session_transaction() as sess:
        assert sess['username'] == 'testuser'
    
    assert response.status_code == 302
    assert url_for('profile') in response.location

def test_signup_get(client) -> None :
    """ Test the signup GET request """
    response = client.get(url_for('auth.signup'))
    assert response.status_code == 200
    assert b'signup.html' in response.data

@patch('auth.get_db')
def test_signup_post(mock_get_db, client: FlaskClient) -> None :
    """ Test the signup POST request """
    # Simulate a successful signup by not throwing any database errors
    response = client.post(url_for('auth.signup'), data={
        'username': 'newuser',
        'password': 'newpass'
    })
    assert response.status_code == 302
    assert url_for('auth.login') in response.location

def test_logout(client: FlaskClient) -> None:
    """ Test the logout """
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'
    response = client.get(url_for('auth.logout'))
    assert response.status_code == 302
    assert url_for('auth.login') in response.location
    with client.session_transaction() as sess:
        assert 'username' not in sess

def create_app() -> None :
    """ Create an mock app """
    from flask import Flask
    app = Flask(__name__)
    app.secret_key = 'testsecretkey'
    return app

def create_test_db_schema(db):
    """ Create a mock db """
    with db.cursor() as cursor:
        # Create the `user` table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `user` (
                `email` VARCHAR(255) PRIMARY KEY,
                `username` VARCHAR(255) NOT NULL,
                `password` VARCHAR(255) NOT NULL
            );
        """)
        db.commit()