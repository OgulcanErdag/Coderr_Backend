from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from authentication_app.models import UserProfile
from offer_app.models import Offer, OfferDetail
from django.db.models import Min

class OfferMinPriceFilterTestCase(APITestCase):
    def setUp(self):
       
        self.user = User.objects.create_user(username="biz", password="biz123", email="biz@example.com")
        UserProfile.objects.create(user=self.user, type="business")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        offer1 = Offer.objects.create(user=self.user, title="Low Price", description="cheap")
        OfferDetail.objects.create(offer=offer1, offer_type="basic", price=50, delivery_time_in_days=5, revisions=1, features=["feature"])
        OfferDetail.objects.create(offer=offer1, offer_type="standard", price=100, delivery_time_in_days=5, revisions=1, features=["feature"])
        OfferDetail.objects.create(offer=offer1, offer_type="premium", price=150, delivery_time_in_days=5, revisions=1, features=["feature"])

        offer2 = Offer.objects.create(user=self.user, title="High Price", description="expensive")
        OfferDetail.objects.create(offer=offer2, offer_type="basic", price=120, delivery_time_in_days=5, revisions=1, features=["feature"])
        OfferDetail.objects.create(offer=offer2, offer_type="standard", price=300, delivery_time_in_days=5, revisions=1, features=["feature"])
        OfferDetail.objects.create(offer=offer2, offer_type="premium", price=600, delivery_time_in_days=5, revisions=1, features=["feature"])

    def test_min_price_filter_excludes_low_price_offer(self):
        url = "/api/offers/?min_price_offer=75"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        offers = response.data['results']

        for offer in offers:
            min_price = float(offer["min_price"])
            self.assertGreaterEqual(min_price, 75, f"min_price {min_price} is less than 75")

        titles = [o["title"] for o in offers]
        self.assertIn("High Price", titles)
        self.assertNotIn("Low Price", titles)
