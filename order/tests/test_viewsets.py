from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class OrderViewSetAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="secret123",
        )
        self.token = Token.objects.create(user=self.user)

    def test_orders_endpoint_requires_token_authentication(self):
        response = self.client.get("/bookstore/v1/orders/")

        self.assertEqual(response.status_code, 401)

    def test_orders_endpoint_accepts_token_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get("/bookstore/v1/orders/")

        self.assertEqual(response.status_code, 200)
