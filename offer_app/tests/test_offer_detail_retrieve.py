from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from offer_app.models import Offer, OfferDetail
from rest_framework import status
from decimal import Decimal

class OfferDetailRetrieveTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.offer = Offer.objects.create(
            user=self.user, 
            title="Test Offer", 
            description="Test Offer Description"
        )
        self.detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5, 
            price=100,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic"
        )
        
        self.url = reverse("offer-detail-type", kwargs={"pk": self.detail.pk})
        self.client = APIClient()  

    def test_offer_detail_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data["id"], self.detail.id)
        self.assertEqual(response.data["title"], self.detail.title)
        self.assertEqual(response.data["revisions"], self.detail.revisions)
        self.assertEqual(response.data["delivery_time_in_days"], self.detail.delivery_time_in_days)
        self.assertEqual(Decimal(response.data["price"]), self.detail.price)
        self.assertEqual(response.data["offer_type"], self.detail.offer_type)
        self.assertIn("features", response.data)
        self.assertEqual(response.data["features"], self.detail.features)
