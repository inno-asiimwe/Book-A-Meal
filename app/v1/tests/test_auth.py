import unittest
import json
from manage import start_app
from app.v1.models.db_connect import db

app = start_app()


class AuthTestCase(unittest.TestCase):
    """test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = app
        self.client = self.app.test_client
        self.user_data = {
            "email": "ronald@gmail.com",
            "password": "U1nhackable"
        }

        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_registration(self):
        """Test user registration works correctly."""
        response = self.client().post('/auth/register', content_type="application/json", data=json.dumps(self.user_data))
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        response = self.client().post('/auth/register', content_type="application/json", data=json.dumps(self.user_data))
        result = json.loads(response.data.decode())
        response = self.client().post("/auth/register", data=self.user_data)
        result = json.loads(response.data.decode())
        self.assertIn(
            "User already exists. Please login.", result)

    def test_registration_with_token_like_password(self):
        """tests wether a user can register with invalid password"""
        user_data = {
            "email": "ronald@gmail.com",
            "password": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MzA5\
            ODAyNDIsInN1YiI6Nn0.FDWEgSrNXmt6r_8ocwVbMRbU1h9u76w-ZhQ71SoJJus"
        }
        response = self.client().post("/auth/register", data=user_data)
        result = json.loads(response.data.decode())
        self.assertIn(
            u'Length must be between 8 and 100.', response.data)

    def test_registration_with_wrong_email(self):
        """tests wether a user can register with invalid password"""
        user_data = {
            "email": "ronald @gmail.com",
            "password": "eyJ0eXAiOiJKV1"
        }
        response = self.client().post("/auth/register", data=user_data)
        result = json.loads(response.data.decode())
        self.assertIn(
            u'Not a valid email address', response.data)

    def test_registration_with_short_like_password(self):
        """tests wether a user can register with invalid password"""
        user_data = {
            "email": "ronald@gmail.com",
            "password": "eyJ0"
        }
        response = self.client().post("/auth/register", data=user_data)
        result = json.loads(response.data.decode())
        self.assertIn(
            u'Length must be between 8 and 100.', response.data)

    def test_user_login(self):
        """Test registered user can login."""
        self.client().post("/auth/register", data=self.user_data)
        login_response = self.client().post("/auth/login", data=self.user_data)
        result = json.loads(login_response.data.decode())
        self.assertEqual(result["message"], "You logged in successfully.")
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(result["access_token"])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        not_a_user = {
            "email": "hacker@gmail.com",
            "password": "badguy"
        }
        response = self.client().post("/auth/login", data=not_a_user)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 500)
        self.assertIn(
            "Please register then login", response.data)
