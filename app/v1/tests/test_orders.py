import unittest
import json
from manage import start_app
from app.v1.models.db_connect import db

app = start_app()


class OrderTestCase(unittest.TestCase):
    """This class represents the order test case"""

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

    def test_get_all_orders(self):
        """tests api ability to retrieve orders"""
        self.client().post("/auth/register", data=self.user_data)
        login_response = self.client().post("/auth/login", data=self.user_data)
        result = json.loads(login_response.data.decode())
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
        order_response = self.client().post(
            "/api/v1/orders"
        )
        self.assertEqual(201, order_response.status_code)
        

    def test_make_orders(self):
        """tests api ability to retrieve orders"""
        self.client().post("/auth/register", data=self.user_data)
        login_response = self.client().post("/auth/login", data=self.user_data)
        result = json.loads(login_response.data.decode())
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
        order_response = self.client().post(
            "/api/v1/orders"
        )
        self.assertEqual(200, order_response.status_code)

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
