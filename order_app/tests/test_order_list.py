from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from order_app.models import Order
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status

class OrderListTestCase(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username="customer1", password="pass123")
        self.business = User.objects.create_user(username="business1", password="pass123")
        
        from authentication_app.models import UserProfile
        UserProfile.objects.create(user=self.customer, type="customer")
        UserProfile.objects.create(user=self.business, type="business")
        
        self.token = Token.objects.create(user=self.customer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
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
      
        self.order2 = Order.objects.create(
            customer_user=self.business, 
            business_user=self.customer,
            title="Flyer Design",
            revisions=2,
            delivery_time_in_days=3,
            price=100,
            features=["Flyer"],
            offer_type="basic",
            status="completed"
        )
        
        self.url = reverse("order-list-create")
    
    def test_order_list_returns_orders_for_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(order["id"] == self.order1.id for order in response.data["results"]))
        self.assertTrue(any(order["id"] == self.order2.id for order in response.data["results"]))

