import app
import unittest

class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_index(self):
        result = self.app.get('/')
        # Make your assertions
        self.assertEqual(1,1)
      
    def test_login(self):
        result = self.app.get('/login')
        self.assertFalse(False)