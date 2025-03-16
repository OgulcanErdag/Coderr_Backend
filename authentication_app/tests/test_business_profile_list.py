from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse

class BusinessProfileListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='biztester',
            password='testpass'
        )
        self.business_profile = UserProfile.objects.create(
            user=self.user,
            type='business',
            location='Stuttgart'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('business-profiles')

    def test_get_business_profiles(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        usernames = [profile['username'] for profile in response.data]
        self.assertIn(self.user.username, usernames)

        for profile in response.data:
            self.assertEqual(profile['type'], 'business')
