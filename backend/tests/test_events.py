import pytest
from flask import url_for
from unittest.mock import patch

from app import create_app

# Setup the Flask test client
@pytest.fixture
def client():
    app = create_app()

    # Use the TEST configuration if available
    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as client:
        with app.app_context():
            # Initialize the test database here
            init_db_for_tests(app)
        yield client

# Test the GET request for the event creation page
def test_event_creation_page(client):
    # Simulate a logged-in user
    with client.session_transaction() as sess:
        sess['user_id'] = 1  
    response = client.get(url_for('events.create_event'))
    assert response.status_code == 200
    assert b'Event Creation Form' in response.data  # Check for form content

# Test the POST request for creating an event
@patch('events.get_db')
def test_create_event(mock_get_db, client):
    # Setup the mock to simulate a database
    mock_cursor = mock_get_db.return_value.cursor.return_value
    mock_cursor.execute.return_value = None
    mock_cursor.fetchone.return_value = None  # Simulate no return value for insert operations
    
    # Simulate a logged-in user
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    
    # Simulate form data for creating an event
    form_data = {
        'title': 'Test Event',
        'description': 'This is a test event',
        # Add other form fields as necessary
    }
    
    response = client.post(url_for('events.create_event_request'), data=form_data)
    assert response.status_code == 302  # Assuming redirect after event creation
    assert url_for('events.view_event') in response.location  # Assuming there is a route to view the event

# Initializing the db connection
def init_db_for_tests(app):
    app.config['DB_HOST'] = 'test_db_host'
    app.config['DB_PORT'] = 'test_db_port'
    app.config['DB_USER'] = 'test_db_user'
    app.config['DB_PASSWORD'] = 'test_db_password'
    app.config['DB_NAME'] = 'test_db_name'

# Create the schema for test
def create_test_db_schema(db):
    with db.cursor() as cursor:
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