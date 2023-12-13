import pytest
from flask import url_for
from flask.testing import FlaskClient
from unittest.mock import patch
import sys
sys.path.append('./backend')
from ..app import create_app
from blueprints.groups import groups_blueprint

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

@pytest.mark.pytests
def test_create_team_accessibility(test_client: FlaskClient) -> None:
    response = test_client.get('/create_team')

    assert response.status_code == 200
    assert 'create_teams' in response.data.decode()

@pytest.mark.pytests
def test_create_group_post(test_client: FlaskClient) -> None:
    with test_client as client:
        with client.session_transaction() as sess:
            sess['email'] = 'testuser@example.com'

        data = {
            'groupName': 'Test Group',
            'groupDescription': 'test group'
        }

        response = client.post('/create_group', data=data)

        assert response.status_code == 302
        assert url_for('auth.home') in response.location

@pytest.mark.pytests
def test_group_page_get(test_client: FlaskClient) -> None:
    group_id = 1  # mock as 1

    with test_client as client:
        with client.session_transaction() as sess:
            sess['email'] = 'testuser@example.com'

        response = client.get(f'/group/{group_id}')

        assert response.status_code == 200 or response.status_code == 302
