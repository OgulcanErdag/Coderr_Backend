from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from authentication_app.models import UserProfile
from offer_app.models import Offer, OfferDetail
from rest_framework import status
from decimal import Decimal

class OfferDetailTestCase(APITestCase):
    def setUp(self):
        # Business-User erstellen
        self.user = User.objects.create_user(username='biz_user', password='test123')
        UserProfile.objects.create(user=self.user, type='business')
        self.token = Token.objects.create(user=self.user)
        
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Angebot erstellen
        self.offer = Offer.objects.create(
            user=self.user,
            title="Design Paket",
            description="Professionelles Grafikdesign"
        )
        
        # OfferDetail erstellen und als self.detail speichern
        self.detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic",
            price=100,
            delivery_time=5,
            revisions=2,
            features=["Logo"],
            offer_type="basic"
        )
        
        # URL für den GET-Request vorbereiten – verwende die ID des OfferDetail-Objekts
        self.url = reverse("offer-detail", kwargs={"pk": self.detail.pk})

    def test_get_offer_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.detail.id)
        self.assertEqual(response.data["title"], self.detail.title)
        self.assertEqual(response.data["revisions"], self.detail.revisions)
        self.assertEqual(response.data["delivery_time_in_days"], self.detail.delivery_time)
        self.assertEqual(Decimal(response.data["price"]), self.detail.price)
        self.assertEqual(response.data["offer_type"], self.detail.offer_type)
        self.assertIn("features", response.data)
        self.assertEqual(response.data["features"], self.detail.features)
