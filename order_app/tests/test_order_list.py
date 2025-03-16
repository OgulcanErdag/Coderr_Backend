from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from order_app.models import Order
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status

class OrderListTestCase(APITestCase):
    def setUp(self):
        # Erstelle zwei Benutzer
        self.customer = User.objects.create_user(username="customer1", password="pass123")
        self.business = User.objects.create_user(username="business1", password="pass123")
        
        # Erstelle Profile für beide
        from authentication_app.models import UserProfile
        UserProfile.objects.create(user=self.customer, type="customer")
        UserProfile.objects.create(user=self.business, type="business")
        
        # Erstelle Token für einen der beiden, um den authentifizierten Nutzer zu simulieren
        self.token = Token.objects.create(user=self.customer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Erstelle einige Bestellungen:
        # Bestellung, bei der der Kunde unser Customer ist und Business unser Business-User
        self.order1 = Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title="Logo Design",
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=["Logo Design", "Visitenkarten"],
            offer_type="basic",
            status="in_progress"
        )
        # Bestellung, bei der der authentifizierte User als Business beteiligt ist
        self.order2 = Order.objects.create(
            customer_user=self.business,  # Kunde ist business (zum Testen, aber eigentlich sollte der Kunde ein anderer User sein)
            business_user=self.customer,
            title="Flyer Design",
            revisions=2,
            delivery_time_in_days=3,
            price=100,
            features=["Flyer"],
            offer_type="basic",
            status="completed"
        )
        
        self.url = reverse("order-list")
    
    def test_order_list_returns_orders_for_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Es sollten alle Bestellungen zurückgegeben werden, bei denen der authentifizierte Nutzer beteiligt ist
        # In unserem Setup ist self.customer entweder als customer in order1 oder als business in order2 beteiligt.
        self.assertTrue(any(order["id"] == self.order1.id for order in response.data["results"]))
        self.assertTrue(any(order["id"] == self.order2.id for order in response.data["results"]))

