from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse

class CustomerProfileListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='customertester',
            password='testpass'
        )
        self.customer_profile = UserProfile.objects.create(
            user=self.user,
            type='customer',
            location='Köln'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('customer-profiles')

    def test_get_customer_profiles(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(p['username'] == self.user.username for p in response.data))
        self.assertTrue(all(p['type'] == 'customer' for p in response.data))
