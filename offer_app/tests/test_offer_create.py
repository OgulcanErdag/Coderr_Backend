from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from authentication_app.models import UserProfile


class OfferCreateTestCase(APITestCase):

    def setUp(self):
        # 🔐 Business-User anlegen
        self.user = User.objects.create_user(username="biz", password="biz123", email="biz@example.com")
        UserProfile.objects.create(user=self.user, type="business")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.url = "/api/offers/"  

    def test_business_user_can_create_offer(self):
        payload = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 250,
                    "features": ["Logo Design", "Visitenkarte", "Social Media Kit"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Flyer", "Website Mockup"],
                    "offer_type": "premium"
                }
            ]
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Grafikdesign-Paket")
        self.assertEqual(len(response.data["details"]), 3)
