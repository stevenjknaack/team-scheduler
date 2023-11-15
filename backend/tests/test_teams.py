""" Test routes and functions of teams.py """

import pytest
from flask import url_for, Flask, FlaskClient
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client() -> None :
    """ Set up testing client """
    app: Flask = create_app()

    # Use the TEST configuration if available
    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as client:
        with app.app_context():
            # Initialize the test database here
            init_db_for_tests(app)
        yield client

def test_team_creation_page(client: FlaskClient) -> None :
    """ Test the GET request for the team creation page """
    # Simulate a logged-in user with sufficient permissions
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # assuming a user ID is stored in the session when logged in
        sess['is_admin'] = True  # assuming a flag for admin role
    response = client.get(url_for('teams.create_team'))
    assert response.status_code == 200
    assert b'Team Creation Form' in response.data  # Check for form content


@patch('teams.get_db')
def test_create_team(mock_get_db, client: FlaskClient) -> None :
    """ Test the POST request for creating a new team """
    # Setup the mock to simulate a database
    mock_cursor = mock_get_db.return_value.cursor.return_value
    mock_cursor.execute.return_value = None
    mock_cursor.fetchone.return_value = None  # Simulate no return value for insert operations
    
    # Simulate a logged-in user with sufficient permissions
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['is_admin'] = True
    
    # Simulate form data for creating a new team
    form_data = {
        'team_name': 'New Team',
        'team_description': 'This is a new team',
        # Add other form fields as necessary
    }
    
    response = client.post(url_for('teams.create_team_request'), data=form_data)
    assert response.status_code == 302  # Assuming redirect after team creation
    assert url_for('teams.view_team') in response.location  # Assuming there is a route to view the team

def init_db_for_tests(app: Flask) -> None:
    """ Placeholder for initializing the test database """
    # Configure the test database settings here
    app.config['DB_HOST'] = 'test_db_host'
    app.config['DB_PORT'] = 'test_db_port'
    app.config['DB_USER'] = 'test_db_user'
    app.config['DB_PASSWORD'] = 'test_db_password'
    app.config['DB_NAME'] = 'test_db_name'

def create_test_db_schema(db) -> None:
    """ Initialize the test database schema here """
    with db.cursor() as cursor:
        
    # Create the `team` table.
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS `team` (
                    `team_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                    `team_name` VARCHAR(255) NOT NULL,
                    `team_description` TEXT,
                    `group_id` INTEGER NOT NULL,
                    FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`)
                    ON UPDATE CASCADE ON DELETE CASCADE
                );
            """)
        
        # Now create the `event` table as you provided.
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS `event` (
                    `event_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                    `event_name` VARCHAR(255) NOT NULL DEFAULT 'Unnamed Event',
                    `start_date` DATE NOT NULL,
                    `end_date` DATE NOT NULL,
                    `reg_start_day` ENUM('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'),
                    `reg_end_day` ENUM('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'),
                    `start_time` TIME NOT NULL,
                    `end_time` TIME NOT NULL,
                    `event_description` TEXT,
                    `edit_permission` ENUM('member', 'group_admin') NOT NULL DEFAULT 'group_admin',
                    `group_id` INTEGER NOT NULL,
                    `team_id` INTEGER,
                    CHECK ((`reg_start_day` IS NULL AND `reg_end_day` IS NULL)
                    XOR (`reg_start_day` IS NOT NULL AND `reg_end_day` IS NOT NULL)),
                    FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (`team_id`, `group_id`) REFERENCES `team` (`team_id`, `group_id`)
                    ON UPDATE CASCADE ON DELETE CASCADE
                );
            """)
        db.commit()


