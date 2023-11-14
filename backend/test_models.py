""" 
Unit testing for models.py 

:author: Steven Knaack
"""

from models import *
import unittest
import os
from models import *
from datetime import time
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
        #self.db: SQLAlchemy =\
        #    models.configure_flask_sqlalchemy(self.real_app)

        # set up SQLAlchemy object
        self.db: SQLAlchemy =\
            configure_flask_sqlalchemy(self.real_app)
        self.db: SQLAlchemy =\
            configure_flask_sqlalchemy(self.real_app)
        self.app = self.real_app.test_client()
    
    def test_membership(self) -> None :
        """ test the Membership model """
        with self.app.application.app_context() :
            steven = self.db.session.get(User, 'sjk@gmail.com')
            print(steven.memberships)
        
    def test_user(self) -> None :
        """ test the User model """
        with self.app.application.app_context() : 
            steven: User =\
                self.db.session.get(User, 'sjk@gmail.com')
            print(steven)
            steven.username = 'knaack'
            self.db.session.commit()

            knaack: User =\
                self.db.session.get(User, 'sjk@gmail.com')
            print(knaack)
        pass

    def test_availability_block(self) -> None :
        """ test the Availability model """
        """ with self.app.application.app_context() :
            user = self.db.session.get(User, 'sjk@gmail.com')
            ab = AvailabilityBlock('tuesday', 'wednesday', time(10,10,10), time(10,20,10), user.email)
            self.db.session.add(ab)
            self.db.session.commit()
            print(str(user.availability_blocks))"""
        pass

    def test_group(self) -> None :
        """ test the Group model """
        with self.app.application.app_context() :
            new_group = Group('sjk\'s group', 'my first group')
            self.db.session.add(new_group)
            self.db.session.commit()

            steven = self.db.session.get(User, 'sjk@gmail.com')
            steven.memberships.append(Membership(steven.email, new_group.id, 'owner'))
            self.db.session.commit()

            print(steven.memberships)
        
    def test_team(self) -> None :
        """ test the Team model """
        pass

    def test_event(self) -> None :
        """ test the Event model """
        pass


if __name__ == '__main__':
    unittest.main()

