""" 
Unit testing for models.py 

:author: Steven Knaack
"""

import models
import unittest
import os
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class MyTestCase(unittest.TestCase) :

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

        # set up SQLAlchemy object
        self.db: SQLAlchemy =\
            models.configure_flask_sqlalchemy(self.real_app)
        self.app = self.real_app.test_client()
    
    def test_membership(self) -> None :
        """ test the Membership model """
        pass

    def test_user(self) -> None :
        """ test the User model """
        with self.app.application.app_context() :
            #new_user = models.User('test2@gmail.com', 'test', 'test')
            #self.db.session.add(new_user)
            #self.db.session.commit()
            steven: models.User =\
                self.db.session.get(models.User, 'Steven@gmail.com')
            print(steven)

    def test_availability_block(self) -> None :
        """ test the Availability model """
        pass

    def test_group(self) -> None :
        """ test the Group model """
        pass

    def test_team(self) -> None :
        """ test the Team model """
        pass

    def test_event(self) -> None :
        """ test the Event model """
        pass


if __name__ == '__main__':
    unittest.main()

