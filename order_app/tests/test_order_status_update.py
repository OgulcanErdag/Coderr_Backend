from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from order_app.models import Order
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status

class OrderStatusUpdateTestCase(APITestCase):
    def setUp(self):
        # Erstelle einen Business-Nutzer
        self.business_user = User.objects.create_user(username="bizupdate", password="update123")
        UserProfile.objects.create(user=self.business_user, type="business")
        self.token = Token.objects.create(user=self.business_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Erstelle eine Bestellung (Order)
        # Hier simulieren wir, dass der Business-Nutzer als Geschäftspartner involviert ist
        # und der Kunde ein anderer User ist
        self.customer_user = User.objects.create_user(username="customerX", password="cust123")
        UserProfile.objects.create(user=self.customer_user, type="customer")
        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Logo Design",
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=["Logo Design", "Visitenkarten"],
            offer_type="basic",
            status="in_progress"
        )
        # URL zum Aktualisieren des Bestellstatus
        self.url = reverse("order-status-update", kwargs={"pk": self.order.pk})

    def test_business_user_can_update_order_status(self):
        payload = {"status": "completed"}
        response = self.client.patch(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")
