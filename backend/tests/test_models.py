""" 
Unit testing for models.py 

:author: Steven Knaack
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
"""
print("In module products __package__, __name__ ==", __package__, __name__)
from ..models import *
import unittest
import os
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

        # set up SQLAlchemy object
        self.db: SQLAlchemy =\
            configure_flask_sqlalchemy(self.real_app)
            
        self.app = self.real_app.test_client()
    
    def test_membership(self) -> None :
        """ test the Membership model """
        with self.app.application.app_context() :
            # pre
            user_create_email = 'testuser@gmail.com'
            user_create_username = 'testuser'
            user_create_password = 'password'
            user_create = User(user_create_email, user_create_username, user_create_password)
            self.db.session.add(user_create)
            self.db.session.commit()

            fail_membership = Membership('', 0)

            # test create
            membership_create_email = 'testuser@gmail.com'
            membership_create_group_id = 10000
            membership_create_role = 'owner'
            membership_create = Membership(membership_create_email,
                                            membership_create_group_id, membership_create_role)
            self.db.session.add(membership_create)
            self.db.session.commit()

            # test read 
            membership_read = self.db.session.get(Membership, membership_create_email) or fail_membership
            self.assertEqual(membership_create_email, membership_read.user_email)
            self.assertEqual(membership_create_group_id, membership_read.group_id)
            self.assertEqual(membership_create_role, membership_read.role)

            # test update
            new_membership_read_role = 'invitee'
            membership_read.role = new_membership_read_role
            self.db.session.commit()
            membership_read = self.db.session.get(Membership, new_membership_read_role) or fail_membership
            self.assertEqual(membership_read.role, new_membership_read_role)

            # test delete
            self.db.session.delete(membership_read)
            self.db.session.commit()
            
            self.assertIsNone(self.db.session.get(Membership, membership_create_email))
           

    def test_user(self) -> None :
        """ test the User model """
        with self.app.application.app_context() :
            # define a fail user
            fail_user = User('fail', 'fail', 'fail')

            # test create
            user_create_email = 'testuser@gmail.com'
            user_create_username = 'testuser'
            user_create_password = 'password'
            user_create = User(user_create_email, user_create_username, user_create_password)
            self.db.session.add(user_create)
            self.db.session.commit()

            # test read 
            user_read = self.db.session.get(User, user_create_email) or fail_user
            self.assertEqual(user_create_email, user_read.email)
            self.assertEqual(user_create_username, user_read.username)
            self.assertEqual(user_create_password, user_read.password)

            # test update
            new_user_read_email = 'newtestuser@gmail.com'
            user_read.email = new_user_read_email
            self.db.session.commit()
            user_read = self.db.session.get(User, new_user_read_email) or fail_user
            self.assertEqual(user_read.email, new_user_read_email)

            new_user_read_username = 'newtestuser'
            user_read.username = new_user_read_username
            self.db.session.commit()
            user_read = self.db.session.get(User, new_user_read_email) or fail_user
            self.assertEqual(user_read.username, new_user_read_username)

            new_user_read_password = 'newpassword'
            user_read.password = new_user_read_password
            self.db.session.commit()
            user_read = self.db.session.get(User, new_user_read_email) or fail_user
            self.assertEqual(user_read.password, new_user_read_password)

            # test delete
            user_delete_email = 't@email.com'
            user_delete = User(user_delete_email, 't', 't')
            self.db.session.add(user_delete)
            self.db.session.commit()

            self.db.session.delete(user_delete)
            self.db.session.commit()
            
            self.assertIsNone(self.db.session.get(User, user_delete_email))

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
        """
        with self.app.application.app_context() :
            new_group = Group('sjk\'s group', 'my first group')
            self.db.session.add(new_group)
            self.db.session.commit()

            steven = self.db.session.get(User, 'sjk@gmail.com')
            steven.memberships.append(Membership(steven.email, new_group.id, 'owner'))
            self.db.session.commit()

            print(steven.memberships)
            """
        pass
        
    def test_team(self) -> None :
        """ test the Team model """
        pass

    def test_event(self) -> None :
        """ test the Event model """
        pass 


if __name__ == '__main__':
    unittest.main()

