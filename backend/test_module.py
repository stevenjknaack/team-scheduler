import app
import unittest
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv


class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_index(self):
        result = self.app.get('/')
        # Make your assertions
        self.assertEqual(1,1)

    def test_signup_page(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
      
    def test_login(self):
        result = self.app.get('/login')
        self.assertEqual(result.status_code, 200)

    #Test the 'create_event' page
    def test_create_event_page(self):
        response = self.app.get('/create-event')
        self.assertEqual(response.status_code, 302)

    """ Test creating an event via 'create_event_request'"""
    def test_create_event_request(self):
        """ Simulate a signed-in user """
        with self.app as client:
            user_data = {
                'email': 'dk@gmail.com',
                'password': 'krovas'
            }
            response = client.post('/login-request', data=user_data)
            """ Check for successful login """
            self.assertEqual(response.status_code, 200)

            """ Data for creating an event """
            event_data = {
                'event_name': 'Test Event',
                'event_description': 'This is a test event description',
                'start_day': '01',
                'start_month': '01',
                'start_year': '2023',
                'end_day': '02',
                'end_month': '01',
                'end_year': '2023'
            }

            """ Use the test client to post the event creation request"""
            response = client.post('/create-event-request', data=event_data, follow_redirects=True)
            # Assuming a successful redirect upon event creation
            self.assertEqual(response.status_code, 200)

    # Assuming a successful redirect upon event creation
    # Test logging in with valid credentials.
    def test_login_valid_credentials(self):
        valid_credentials = {
            'email': 'dk@gmail.com',  
            'password': 'krovas'     
        }
        response = self.app.post('/login-request', data=valid_credentials, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # TODO: test router

    # Test logging in with invalid credentials
    def test_login_invalid_credentials(self):
        invalid_credentials = {
            'email': 'test@gmail.com',  
            'password': 'wrongpassword'
        }
        response = self.app.post('/login-request', data=invalid_credentials)
        self.assertEqual(response.status_code, 401)

    # Test logging in with nonexistent account
    def test_login_nonexistent_user(self):
        nonexistent_user = {
            'email': 'nonexistent@gmail.com', 
            'password': 'test'
        }
        response = self.app.post('/login-request', data=nonexistent_user)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()

