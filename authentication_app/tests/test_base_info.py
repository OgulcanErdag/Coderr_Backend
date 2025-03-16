from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BaseInfoTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ogicoderr", password="secretpass123")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_base_info_returns_data(self):
        url = reverse("base-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("review_count", response.data)
        self.assertIn("average_rating", response.data)
        self.assertIn("business_profile_count", response.data)
        self.assertIn("offer_count", response.data)
