from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from review_app.models import Review
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status

class ReviewCreateTestCase(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username="custuser", password="custpass")
        UserProfile.objects.create(user=self.customer, type="customer")
        
        self.business = User.objects.create_user(username="bizuser", password="bizpass")
        UserProfile.objects.create(user=self.business, type="business")
        
        self.token = Token.objects.create(user=self.customer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.url = reverse("review-create")
    
    def test_review_create_successful(self):
        payload = {
            "business_user": self.business.id,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["business_user"], self.business.id)
        self.assertEqual(response.data["reviewer"], self.customer.id)
        self.assertEqual(response.data["rating"], 4)
        self.assertEqual(response.data["description"], "Alles war toll!")
    
    def test_duplicate_review_not_allowed(self):
        payload = {
            "business_user": self.business.id,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response1 = self.client.post(self.url, payload, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        response2 = self.client.post(self.url, payload, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
