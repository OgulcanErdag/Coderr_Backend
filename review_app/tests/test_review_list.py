from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from review_app.models import Review
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

class ReviewListTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        
        self.token = Token.objects.create(user=self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        self.review1 = Review.objects.create(
            business_user=self.user2,
            reviewer=self.user1,
            rating=4,
            description="Sehr professioneller Service.",
            created_at=timezone.now() - timedelta(days=1),
            updated_at=timezone.now() - timedelta(hours=2)
        )
        self.review2 = Review.objects.create(
            business_user=self.user2,
            reviewer=self.user1,
            rating=5,
            description="Top Qualität und schnelle Lieferung!",
            created_at=timezone.now() - timedelta(days=2),
            updated_at=timezone.now() - timedelta(hours=1)
        )
        self.url = reverse("review-list")

    def test_review_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
