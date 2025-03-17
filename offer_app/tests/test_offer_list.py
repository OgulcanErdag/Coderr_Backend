from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from authentication_app.models import UserProfile
from offer_app.models import Offer, OfferDetail  
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from decimal import Decimal


class OfferListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='offeruser', password='test123')
        UserProfile.objects.create(user=self.user, type="business")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.offer = Offer.objects.create(
            user=self.user,
            title="Test Angebot",
            description="Einfach ein Testangebot"
        )

        OfferDetail.objects.create(offer=self.offer, price=Decimal("100.00"), delivery_time_in_days=5)
        OfferDetail.objects.create(offer=self.offer, price=Decimal("200.00"), delivery_time_in_days=10)

        self.url = reverse("offer-list")

    def test_offer_list_returns_offer_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)

        offer = response.data["results"][0]
        self.assertEqual(offer["title"], "Test Angebot")
        self.assertEqual(offer["description"], "Einfach ein Testangebot")

        self.assertIn("details", offer)
        self.assertEqual(len(offer["details"]), 2)

        self.assertIn("min_price", offer)
        self.assertEqual(Decimal(offer["min_price"]), Decimal("100.00")) 

        self.assertIn("min_delivery_time", offer)
        self.assertEqual(offer["min_delivery_time"], 5)

        self.assertIn("user", offer)
        self.assertEqual(offer["user"], self.user.id)

