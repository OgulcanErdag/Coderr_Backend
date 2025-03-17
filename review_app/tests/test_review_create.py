from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status

from authentication_app.models import UserProfile
from offer_app.models import Offer, OfferDetail
from order_app.models import Order
from review_app.models import Review


class TestReviewCreate(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username="custuser", password="custpass")
        UserProfile.objects.create(user=self.customer, type="customer")
        
        self.business = User.objects.create_user(username="bizuser", password="bizpass")
        UserProfile.objects.create(user=self.business, type="business")
        
        self.token = Token.objects.create(user=self.customer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.offer = Offer.objects.create(user=self.business, title="Design", description="Logo Design")
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Logo Basic",
            revisions=2,
            delivery_time_in_days=3,
            price=100,
            features=["Logo"],
            offer_type="basic"
        )

        self.order = Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            offer_detail=self.offer_detail,
            title="Logo Basic",
            revisions=2,
            delivery_time_in_days=3,
            price=100,
            features=["Logo"],
            offer_type="basic",
            status="completed"
        )

        self.url = "/api/reviews/"

    def test_review_create_successful(self):
        payload = {
            "business_user": self.business.id,
            "rating": 5,
            "description": "Super Service!"
        }
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["business_user"], self.business.id)
        self.assertEqual(response.data["reviewer"], self.customer.id)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["description"], "Super Service!")

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
