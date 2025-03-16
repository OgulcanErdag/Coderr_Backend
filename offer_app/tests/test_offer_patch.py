from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from offer_app.models import Offer, OfferDetail
from authentication_app.models import UserProfile
from django.urls import reverse

class OfferPatchTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bizpatch", password="123456")
        UserProfile.objects.create(user=self.user, type="business")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.offer = Offer.objects.create(user=self.user, title="Altes Angebot", description="Altbeschreibung")
        self.detail = OfferDetail.objects.create(offer=self.offer, title="Alt", price=100, revisions=1, delivery_time=5, features=["Logo"], offer_type="basic")
        self.url = reverse("offer-update", kwargs={"pk": self.offer.pk})

    def test_creator_can_patch_offer(self):
        payload = {
            "title": "Neues Angebot",
            "details": [
                {
                    "id": self.detail.id,  # Achte darauf, dass die ID des Details hier korrekt übergeben wird
                    "title": "Neues Detail",
                    "revisions": 2,
                    "delivery_time_in_days": 4,
                    "price": 150,
                    "features": ["Logo", "Flyer"],
                    "offer_type": "basic"
                }
            ]
        }

        response = self.client.patch(self.url, payload, format="json")
        print(response.data)  # Für zusätzliche Debugging-Informationen

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Neues Angebot")
        self.assertEqual(response.data["details"][0]["title"], "Neues Detail")
