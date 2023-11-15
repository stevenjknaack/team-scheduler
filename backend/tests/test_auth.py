import pytest
from flask import session, g, url_for
from unittest.mock import patch
from werkzeug.security import generate_password_hash

# Assuming auth.py is in the same directory as this test file
from blueprints.auth import auth_blueprint

# Setup the Flask test client
@pytest.fixture
def client():
    app = create_app()
    app.register_blueprint(auth_blueprint)
    with app.test_client() as client:
        yield client

# Test the redirection behavior of the index route
def test_index_route(client):
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

# Test the login GET request
def test_login_get(client):
    response = client.get(url_for('auth.login'))
    assert response.status_code == 200
    assert b'login.html' in response.data

# Test the login POST request
@patch('auth.get_db')
def test_login_post(mock_get_db, client):
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

# Test the signup GET request
def test_signup_get(client):
    response = client.get(url_for('auth.signup'))
    assert response.status_code == 200
    assert b'signup.html' in response.data

# Test the signup POST request
@patch('auth.get_db')
def test_signup_post(mock_get_db, client):
    # Simulate a successful signup by not throwing any database errors
    response = client.post(url_for('auth.signup'), data={
        'username': 'newuser',
        'password': 'newpass'
    })
    assert response.status_code == 302
    assert url_for('auth.login') in response.location

# Test the logout
def test_logout(client):
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'
    response = client.get(url_for('auth.logout'))
    assert response.status_code == 302
    assert url_for('auth.login') in response.location
    with client.session_transaction() as sess:
        assert 'username' not in sess

def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.secret_key = 'testsecretkey'
    return app

def create_test_db_schema(db):
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