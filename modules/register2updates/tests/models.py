import unittest
from django.test.client import Client
from register2updates.models import Registered2Updates

class register2UpdatesTestCase(unittest.TestCase):
    def setUp(self):
        self.registered_user_email = "test@test.ca"
        self.registered_user = Registered2Updates(email=self.registered_user_email)
        self.registered_user.save()

    def tearDown(self):
        self.registered_user.delete()
    
    def test_if_get_register_validate_existing_user(self):
        self.assertTrue(Registered2Updates.objects.is_registered(self.registered_user_email))
        
    def test_if_get_register_validate_non_existing_user(self):
        self.assertFalse(Registered2Updates.objects.is_registered("test2@test.ca"))

    

class Register2UpdatesViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.c = Client()
        
    def tearDown(self):
        del self.c
        
    def test_add_a_new_email_first_time(self):        
        resp = self.c.get('/register/updates/')
        self.assertEqual(200, resp.status_code)
        
    def test_add_a_new_email_address_complete(self):
        resp = self.c.post('/register/updates/', {'email': 'johm@smith.com', 'email_confirmation': 'john@smith.com'})
        self.assertEqual(200, resp.status_code)
        
    def test_add_a_new_email_address_incomplete(self):
        resp = self.c.post('/register/updates/', {'email': 'johm@smith.com'})
        self.assertEqual(200, resp.status_code)
        
    def test_add_a_new_email_address_password_dont_match(self):
        resp = self.c.post('/register/updates/', {'email': 'johm@smith.com', 'email_confirmation': 'smith@smith.com'})
        self.assertEqual(200, resp.status_code)
        
    def test_add_a_already_existing_email_address(self):
        resp = self.c.post('/register/updates/', {'email': 'johm@smith.com', 'email_confirmation': 'john@smith.com'})
        self.assertEqual(200, resp.status_code)

