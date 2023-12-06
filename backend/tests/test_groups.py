import unittest
from models import *
from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class GroupsBlueprintTestCase(unittest.TestCase):

    def setUp(self) -> None :
        """ 
        setup process for testing 
        
        initializes
            self.app: FlaskClient
            self.db: SQLAlchemy
        for use in the testing
        """
        # set up testing app
        self.real_app = Flask(__name__)
        CORS(self.real_app)
        self.real_app.testing = True
        self.db: SQLAlchemy =\
           models.configure_flask_sqlalchemy(self.real_app)

        # set up SQLAlchemy object
        """
        self.db: SQLAlchemy =\
            configure_flask_sqlalchemy(self.real_app)
            """
        self.app = self.real_app.test_client()

    def tearDown(self):
        # Clean up the database after each test
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_get_group_id_success(self):
        response = self.db.session.get('/get-group-id?group_name=TestGroup')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('group_id', data)

    def test_get_group_id_failure(self):
        response = self.db.session.get('/get-group-id?group_name=NonexistentGroup')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
