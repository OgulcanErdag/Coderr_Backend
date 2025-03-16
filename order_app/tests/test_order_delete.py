from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from order_app.models import Order
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status

class OrderDeleteTestCase(APITestCase):
    def setUp(self):
        # Erstelle einen Staff-Benutzer
        self.admin_user = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
        # Erstelle einen Customer-Nutzer (wird hier nicht löschen dürfen)
        self.customer = User.objects.create_user(username="cust", password="custpass")
        # Erstelle Profile (optional, je nachdem, ob sie benötigt werden)
        from authentication_app.models import UserProfile
        UserProfile.objects.create(user=self.admin_user, type="business")
        UserProfile.objects.create(user=self.customer, type="customer")
        
        # Erstelle Token für Admin
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        
        # Erstelle eine Bestellung, die gelöscht werden soll
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
        self.url = reverse("order-delete", kwargs={"pk": self.order.pk})
    
    def test_admin_can_delete_order(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(pk=self.order.pk)
    
    def test_non_admin_cannot_delete_order(self):
        # Verwende einen Customer-User, um zu löschen
        customer_token = Token.objects.create(user=self.customer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + customer_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
