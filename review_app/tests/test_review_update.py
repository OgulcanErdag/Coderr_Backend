from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from review_app.models import Review
from rest_framework.authtoken.models import Token
from rest_framework import status

class ReviewUpdateTestCase(APITestCase):
    def setUp(self):
        self.reviewer = User.objects.create_user(username="reviewer", password="pass123")    
        self.business = User.objects.create_user(username="biz", password="pass456")
        
        self.review = Review.objects.create(
            business_user=self.business,
            reviewer=self.reviewer,
            rating=3,
            description="Guter Service."
        )
        
        self.token = Token.objects.create(user=self.reviewer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        self.url = reverse("review-details", kwargs={"pk": self.review.id})


    def test_reviewer_can_update_review(self):
        payload = {
            "rating": 5,
            "description": "Noch besser als erwartet!"
        }
        response = self.client.patch(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["description"], "Noch besser als erwartet!")

    def test_non_reviewer_cannot_update_review(self):
        other_user = User.objects.create_user(username="other", password="otherpass")
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + other_token.key)
        
        payload = {
            "rating": 4,
            "description": "Update von einem anderen User"
        }
        response = self.client.patch(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
