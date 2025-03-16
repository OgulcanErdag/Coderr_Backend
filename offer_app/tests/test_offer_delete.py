from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from offer_app.models import Offer
from rest_framework.authtoken.models import Token
from authentication_app.models import UserProfile
from rest_framework import status

class OfferDeleteTestCase(APITestCase):
    def setUp(self):
        # Business-User (Ersteller)
        self.user = User.objects.create_user(username="deletebiz", password="pass123")
        UserProfile.objects.create(user=self.user, type="business")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Angebot des eigenen Users
        self.offer = Offer.objects.create(
            user=self.user,
            title="Angebot zum Löschen",
            description="Dieses Angebot soll gelöscht werden."
        )
        self.url = f"/api/offers/{self.offer.pk}/"

    def test_offer_deletion_successful(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Überprüfen, ob es wirklich gelöscht wurde
        with self.assertRaises(Offer.DoesNotExist):
            Offer.objects.get(pk=self.offer.pk)

    def test_offer_deletion_not_owner(self):
        # Fremder User, der versucht das Angebot zu löschen
        other_user = User.objects.create_user(username="other", password="otherpass")
        UserProfile.objects.create(user=other_user, type="business")
        other_token = Token.objects.create(user=other_user)

        other_offer = Offer.objects.create(
            user=other_user,
            title="Fremdes Angebot",
            description="Dieses Angebot darf nicht gelöscht werden."
        )

        url_other = f"/api/offers/{other_offer.pk}/"

        # Fremder Token setzen
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.delete(url_other)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
