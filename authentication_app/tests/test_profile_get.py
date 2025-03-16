from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse

class UserProfileGetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='gettestuser',
            password='testpassword',
            email='gettest@example.com'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            type='customer',
            location='Berlin'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('profile-detail', kwargs={'pk': self.profile.pk})

    def test_user_can_get_own_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['location'], 'Berlin')
