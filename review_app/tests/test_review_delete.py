from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from review_app.models import Review
from rest_framework.authtoken.models import Token
from rest_framework import status
from authentication_app.models import UserProfile

class ReviewDeleteTestCase(APITestCase):
    def setUp(self):
        self.reviewer = User.objects.create_user(username="reviewer", password="pass123")
        UserProfile.objects.create(user=self.reviewer, type="customer")
 
        self.business = User.objects.create_user(username="business", password="pass456")
        UserProfile.objects.create(user=self.business, type="business")
        
        self.review = Review.objects.create(
            business_user=self.business,
            reviewer=self.reviewer,
            rating=4,
            description="Test Review"
        )
        
        self.token = Token.objects.create(user=self.reviewer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.url = reverse("review-delete", kwargs={"pk": self.review.pk})
        
    def test_reviewer_can_delete_review(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(pk=self.review.pk)
    
    def test_non_reviewer_cannot_delete_review(self):
        other_user = User.objects.create_user(username="other", password="otherpass")
        UserProfile.objects.create(user=other_user, type="customer")
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + other_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
