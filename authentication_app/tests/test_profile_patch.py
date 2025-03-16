from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from authentication_app.models import UserProfile

class UserProfilePatchTestCase(APITestCase):
    def setUp(self):
        # Benutzer 1
        self.user = User.objects.create_user(username="ogicoder", password="secure123")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.profile = UserProfile.objects.create(user=self.user, type="customer")

        # Benutzer 2 (Fremder)
        self.other_user = User.objects.create_user(username="hackerboy", password="hackhack")
        self.other_profile = UserProfile.objects.create(user=self.other_user, type="business")

    def test_user_can_update_own_profile(self):
        url = reverse("profile-detail", kwargs={"pk": self.profile.pk})
        payload = {
            "location": "Berlin",
            "tel": "123456789",
            "description": "Ich bin Ogi",
            "working_hours": "10-18",
            "email": "ogi@coderr.de",
            "first_name": "Ogulcan",
            "last_name": "Dev"
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["location"], "Berlin")
        self.assertEqual(response.data["tel"], "123456789")

    def test_user_cannot_update_foreign_profile(self):
        url = reverse("profile-detail", kwargs={"pk": self.other_profile.pk})
        payload = {
            "location": "Hacked City"
        }

        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, 403)
