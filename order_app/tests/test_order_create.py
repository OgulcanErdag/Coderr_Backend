from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from order_app.models import Order
from offer_app.models import Offer, OfferDetail
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status

class OrderCreateTestCase(APITestCase):
    def setUp(self):
        # Erstelle einen Customer-Nutzer
        self.customer = User.objects.create_user(username="customer1", password="pass123")
        UserProfile.objects.create(user=self.customer, type="customer")
        # Erstelle einen Business-Nutzer
        self.business = User.objects.create_user(username="business1", password="pass123")
        UserProfile.objects.create(user=self.business, type="business")
        # Erstelle Token für den Customer
        self.token = Token.objects.create(user=self.customer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Erstelle ein Angebot durch den Business-Nutzer
        self.offer = Offer.objects.create(
            user=self.business,
            title="Logo Design",
            description="Professionelles Logo Design"
        )
        # Erstelle ein OfferDetail, das als Basis für die Bestellung dient
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Logo Design",
            revisions=3,
            delivery_time=5,
            price=150,
            features=["Logo Design", "Visitenkarten"],
            offer_type="basic"
        )
        self.url = reverse("order-list")
    
    def test_create_order_successfully(self):
        payload = {
            "offer_detail_id": self.offer_detail.id
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Überprüfe, ob das Order-Objekt zurückgegeben wird
        self.assertEqual(response.data["title"], self.offer_detail.title)
        self.assertEqual(response.data["status"], "in_progress")
