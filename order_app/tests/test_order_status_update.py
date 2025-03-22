from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from order_app.models import Order
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status

class OrderStatusUpdateTestCase(APITestCase):
    def setUp(self):
        
        self.business_user = User.objects.create_user(username="bizupdate", password="update123")
        UserProfile.objects.create(user=self.business_user, type="business")
        self.token = Token.objects.create(user=self.business_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
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
     
        self.url = reverse("order-status-update", kwargs={"pk": self.order.pk})

    def test_business_user_can_update_order_status(self):
        payload = {"status": "completed"}
        response = self.client.patch(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")
        self.assertEqual(response.data["title"], "Logo Design")
        self.assertEqual(response.data["revisions"], 3)
        self.assertEqual(response.data["delivery_time_in_days"], 5)
        self.assertEqual(float(response.data["price"]), 150.0)
        self.assertEqual(response.data["features"], ["Logo Design", "Visitenkarten"])
        self.assertEqual(response.data["offer_type"], "basic")
        self.assertEqual(response.data["customer_user"], self.customer_user.id)
        self.assertEqual(response.data["business_user"], self.business_user.id)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
