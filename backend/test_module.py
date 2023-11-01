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

    def test_signup_page(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
      
    def test_login(self):
        result = self.app.get('/login')
        self.assertEqual(result.status_code, 200)
    
    
    # Test create-event-request
    def test_create_event_request(self):
        event_creation = {
            
        }
if __name__ == '__main__':
    unittest.main()

