from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class RegistrationTestCase(APITestCase):

    def test_registration_successful(self):
        url = reverse('register')  

        payload = {
            "username": "ogicoderr",
            "email": "ogi@example.com",
            "password": "securePassword123",
            "repeated_password": "securePassword123",
            "type": "customer"
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertIn("user_id", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data) 
