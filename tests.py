# project/test_basic.py

import os
import unittest

from app.app import Kanban_app
from app.models import db, User, Card

TEST_DB = 'test.db'

class BasicTests(unittest.TestCase):

    # execute before each test
    def setUp(self):
        Kanban_app.config['TESTING'] = True # set test mode
        Kanban_app.config['WTF_CSRF_ENABLED'] = False # enable app to trigger requests
        Kanban_app.config['DEBUG'] = False
        Kanban_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/'+TEST_DB # configure test database
        self.app = Kanban_app.test_client()
        db.drop_all() # drop tables to start fresh for each test
        db.create_all()

        self.assertEqual(Kanban_app.debug, False)

    # execute after each test
    def tearDown(self):
        pass

    # methods to help pass data to views
    def register(self, email, password):
        return self.app.post(
            '/signup',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    # tests to run

    # check home view works
    def test_home(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # test user can register
    def test_registration(self):
        response = self.register('test@gmail.com', 'password')
        # check registration succeeds
        self.assertEqual(response.status_code, 200)
        # check user is redirected to login page
        self.assertIn(b'Login', response.data)

    # test invalid email during registration
    def test_invalid_email(self):
        response = self.register('test', 'password')
        self.assertIn(b'Form didn&#39;t validate', response.data)

    # test invalid passwords during registration
    def test_invalid_password_1(self):
        response = self.register('test', '')
        self.assertIn(b'Form didn&#39;t validate', response.data)

    # test log in works
    def test_valid_login(self):
        response = self.register('test@gmail.com', 'password')
        # check registration succeeds
        self.assertEqual(response.status_code, 200)
        # check use can login details
        response = self.login('test@gmail.com', 'password')
        # check login succeeds
        self.assertEqual(response.status_code, 200)
        #print(response.data)
        #self.assertIn(b'My Kanban', response.data)

    # test incorrect password
    def test_invalid_login_1(self):
        response = self.register('test@gmail.com', 'password')
        # check registration succeeds
        self.assertEqual(response.status_code, 200)
        # check use can login details
        response = self.login('test@gmail.com', 'pssword')
        # check login fails due to password
        self.assertIn(b'Wrong password', response.data)

    # test bad email prevents login
    def test_invalid_login_2(self):
        response = self.register('test@gmail.com', 'password')
        # check registration succeeds
        self.assertEqual(response.status_code, 200)
        # check use can login details
        response = self.login('TT@gmail.com', 'password')
        # check login fails due to email
        self.assertIn(b'User doesn&#39;t exist. Please sign up', response.data)

    # test app prevents duplicate emails
    def test_duplicate_email(self):
        response = self.register('test@gmail.com', 'password')
        self.assertEqual(response.status_code, 200)
        response = self.register('test@gmail.com', 'password')
        self.assertIn(b"Email address already exists", response.data)

    # test logout
    def test_logout(self):
        response = self.register('test@gmail.com', 'password')
        # check registration succeeds
        self.assertEqual(response.status_code, 200)
        # check use can login details
        response = self.login('test@gmail.com', 'password')
        # check login succeeds
        self.assertEqual(response.status_code, 200)
        # check logout succeeds
        self.logout()
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
