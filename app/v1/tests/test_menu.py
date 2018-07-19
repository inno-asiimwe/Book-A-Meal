import unittest
import json
from manage import start_app
from app.v1.models.db_connect import db

app = start_app()


class MenuTestCase(unittest.TestCase):
    """This class represents the menu test case"""

    def setUp(self):
        """Defines the test variables and initializes the app."""
        self.app = app
        self.client = self.app.test_client
        self.meal = {"name": "Beef with Rice", "price": "4500"}
        self.menu = {"meal_id": 1}
        self.user_data = {
            "email": "mutebi@gmail.com",
            "password": "H1ack_it"
        }
        db.create_all()

    def test_setup_menu(self):
        """Tests menu setup"""
        self.client().post("/auth/register", data=self.user_data)
        login_response = self.client().post("/auth/login", data=self.user_data)
        result = json.loads(login_response.data.decode())
        self.assertTrue(result["access_token"])
        self.client().post(
            "/api/v1/meals",
            data=self.meal,
            headers={
                "Authorization": result["access_token"]})
        response = self.client().post(
            "/api/v1/menu",
            data=self.menu,
            headers={
                "Authorization": result["access_token"]})
        self.assertIn(b"Beef with Rice", response.data)

    def test_get_menu(self):
        """Test menu retrieval"""
        self.client().post("/auth/register", data=self.user_data)
        login_response = self.client().post("/auth/login", data=self.user_data)
        result = json.loads(login_response.data.decode())
        self.assertTrue(result['access_token'])
        self.client().post(
            "/api/v1/meals",
            data=self.meal,
            headers={
                "Authorization": result["access_token"]})
        response = self.client().post(
            "/api/v1/menu",
            data=self.menu,
            headers={
                "Authorization": result["access_token"]})
        response = self.client().get("/api/v1/menu",
                                     headers={"Authorization": result["access_token"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Beef with Rice", response.data)

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
