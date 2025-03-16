from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from offer_app.models import Offer, OfferDetail
from rest_framework import status
from decimal import Decimal

class OfferDetailRetrieveTestCase(APITestCase):
    def setUp(self):
        # Einen User erstellen – für das Angebot (Auth ist hier nicht erforderlich, aber zum Verknüpfen nötig)
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Angebot anlegen
        self.offer = Offer.objects.create(
            user=self.user, 
            title="Test Offer", 
            description="Test Offer Description"
        )
        # OfferDetail anlegen
        self.detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Design",
            revisions=2,
            delivery_time=5,  # Im Model heißt das Feld "delivery_time"
            price=100,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic"
        )
        # URL für den GET-Request vorbereiten (Nutze den URL-Namen aus deiner urls.py, z. B. "offer-detail")
        self.url = reverse("offer-detail", kwargs={"pk": self.detail.pk})
        self.client = APIClient()  # Keine Auth nötig, da permission = AllowAny

    def test_offer_detail_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Prüfen, ob die Felder korrekt zurückgegeben werden
        self.assertEqual(response.data["id"], self.detail.id)
        self.assertEqual(response.data["title"], self.detail.title)
        self.assertEqual(response.data["revisions"], self.detail.revisions)
        self.assertEqual(response.data["delivery_time_in_days"], self.detail.delivery_time)
        # Vergleiche den Preis als Decimal, damit "100" und "100.00" als gleich gelten
        self.assertEqual(Decimal(response.data["price"]), self.detail.price)
        self.assertEqual(response.data["offer_type"], self.detail.offer_type)
        self.assertIn("features", response.data)
        self.assertEqual(response.data["features"], self.detail.features)
