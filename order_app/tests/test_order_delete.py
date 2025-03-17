from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from order_app.models import Order
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status

class OrderDeleteTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
        self.customer = User.objects.create_user(username="cust", password="custpass")
        from authentication_app.models import UserProfile
        UserProfile.objects.create(user=self.admin_user, type="business")
        UserProfile.objects.create(user=self.customer, type="customer")
        
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        
        self.order = Order.objects.create(
            customer_user=self.customer,
            business_user=self.admin_user,
            title="Zu löschendes Angebot",
            revisions=2,
            delivery_time_in_days=5,
            price=150,
            features=["Logo Design"],
            offer_type="basic",
            status="in_progress"
        )
        self.url = f"/api/orders/{self.order.pk}/"
    
    def test_admin_can_delete_order(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_non_admin_cannot_delete_order(self):
        customer_token = Token.objects.create(user=self.customer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + customer_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

       
