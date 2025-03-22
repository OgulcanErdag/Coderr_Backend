from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token

class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ogicoderr",
            email="ogi@example.com",
            password="securePassword123"
        )
        self.token = Token.objects.create(user=self.user)

    def test_login_successful(self):
        url = reverse("login")  

        payload = {
            "username": "ogicoderr",
            "password": "securePassword123"
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], self.token.key)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["user_id"], self.user.id)
