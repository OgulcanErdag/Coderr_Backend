from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from order_app.models import Order
from rest_framework.authtoken.models import Token
from authentication_app.models import UserProfile
from rest_framework import status

class CompletedOrderCountTestCase(APITestCase):
    def setUp(self):
        # Erstelle einen Business-Nutzer
        self.business = User.objects.create_user(username="bizcount", password="test123")
        UserProfile.objects.create(user=self.business, type="business")
        # Erstelle einige Bestellungen:
        Order.objects.create(
            customer_user=self.business,
            business_user=self.business,
            title="Order 1",
            revisions=1,
            delivery_time_in_days=5,
            price=100,
            features=["A"],
            offer_type="basic",
            status="completed"
        )
        Order.objects.create(
            customer_user=self.business,
            business_user=self.business,
            title="Order 2",
            revisions=1,
            delivery_time_in_days=5,
            price=200,
            features=["B"],
            offer_type="basic",
            status="completed"
        )
        # Eine Bestellung, die nicht abgeschlossen ist
        Order.objects.create(
            customer_user=self.business,
            business_user=self.business,
            title="Order 3",
            revisions=1,
            delivery_time_in_days=5,
            price=300,
            features=["C"],
            offer_type="basic",
            status="in_progress"
        )
        self.url = reverse("completed-order-count", kwargs={"business_user_id": self.business.id})
    
    def test_completed_order_count(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_order_count"], 2)
