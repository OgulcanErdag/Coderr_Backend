from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from order_app.models import Order
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status

class OrderCountTestCase(APITestCase):
    def setUp(self):
        # Erstelle einen Business-User
        self.business = User.objects.create_user(username="bizcount", password="test123")
        # Erstelle einige Bestellungen mit Status "in_progress"
        Order.objects.create(
            customer_user=self.business,  # Irgendwann musst du hier echte Kunden haben, aber zum Testen reicht's
            business_user=self.business,
            title="Test Order 1",
            revisions=1,
            delivery_time_in_days=5,
            price=100,
            features=["Feature 1"],
            offer_type="basic",
            status="in_progress"
        )
        Order.objects.create(
            customer_user=self.business,
            business_user=self.business,
            title="Test Order 2",
            revisions=1,
            delivery_time_in_days=5,
            price=200,
            features=["Feature 2"],
            offer_type="basic",
            status="in_progress"
        )
        # Erstelle eine Bestellung, die nicht in_progress ist
        Order.objects.create(
            customer_user=self.business,
            business_user=self.business,
            title="Test Order 3",
            revisions=1,
            delivery_time_in_days=5,
            price=300,
            features=["Feature 3"],
            offer_type="basic",
            status="completed"
        )
        self.url = reverse("order-count", kwargs={"business_user_id": self.business.id})
    
    def test_order_count_returns_correct_number(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Es sollten 2 Bestellungen mit Status "in_progress" zurückgegeben werden.
        self.assertEqual(response.data["order_count"], 2)
