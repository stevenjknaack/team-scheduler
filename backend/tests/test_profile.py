import pytest
from flask import session, g, url_for
from flask.testing import FlaskClient
import sys
sys.path.append('./backend')
from app import create_app
from blueprints.auth import auth_blueprint # import obj rather than module
from unittest.mock import patch
from werkzeug.security import generate_password_hash
from models import configure_flask_sqlalchemy, Base, User,AvailabilityBlock
import time
import uuid


# A fixture is where a client is define, we want to simulate requests to the app
@pytest.fixture
def client()-> None :
    app = create_app()
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost:6969'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'
    db = app.db

    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.mark.pytests
def test_save_schedule_post(client: FlaskClient) -> None:
    unique_suffix = str(uuid.uuid4())
    test_email = f"testuser-{unique_suffix}@example.com"
    test_password = "testpass"
    hashed_password = generate_password_hash(test_password)

    with client.application.app_context() as ctx:
        # Assert the application context is active
        # Otherwise context err will pop up
        assert ctx.g is not None

        # Create a new test user
        user = User(email=test_email, username="testuser", password=hashed_password)
        client.application.db.session.add(user)
        client.application.db.session.commit()

    with client.session_transaction() as sess:
        sess['email'] = test_email

    schedule_data = {
        'schedule': [
            {'day': 'Monday', 'startTime': '08:00', 'endTime': '12:00'},
            {'day': 'Tuesday', 'startTime': '13:00', 'endTime': '17:00'}
        ]
    }

    response = client.post(url_for('profile.save_schedule'), json=schedule_data)

    assert response.status_code == 200
    assert response.json['message'] == 'Schedule saved successfully'

    with client.application.app_context():
        client.application.db.session.query(AvailabilityBlock).filter(AvailabilityBlock.user_email == test_email).delete()
        client.application.db.session.delete(user)
        client.application.db.session.commit()

@pytest.mark.pytests
def test_get_schedule_get(client: FlaskClient) -> None:
    unique_suffix = str(uuid.uuid4())
    test_email = f"testuser-{unique_suffix}@example.com"
    test_password = "testpass"
    hashed_password = generate_password_hash(test_password)

    with client.application.app_context():
        # Create a new test user and availability blocks
        user = User(email=test_email, username="testuser", password=hashed_password)
        client.application.db.session.add(user)
        client.application.db.session.commit()

        # Create test availability blocks
        block1 = AvailabilityBlock(start_day='Monday', end_day='Monday', start_time='08:00', end_time='12:00', user_email=test_email)
        block2 = AvailabilityBlock(start_day='Tuesday', end_day='Tuesday', start_time='13:00', end_time='17:00', user_email=test_email)
        client.application.db.session.add_all([block1, block2])
        client.application.db.session.commit()

    with client.session_transaction() as sess:
        # Mock user session
        sess['email'] = test_email

    # Send GET request to get_schedule
    response = client.get(url_for('profile.get_schedule'))

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2  # Assuming two availability blocks were added
    assert data[0]['day'] == 'monday'
    assert data[1]['day'] == 'tuesday'

    with client.application.app_context():
        client.application.db.session.query(AvailabilityBlock).filter(AvailabilityBlock.user_email == test_email).delete()
        client.application.db.session.delete(user)
        client.application.db.session.commit()
