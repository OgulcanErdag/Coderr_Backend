from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='offer_pics/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Offer Media"

class OfferDetail(models.Model):    
    BASIC = 'basic'
    STANDARD = 'standard'
    PREMIUM = 'premium'

    OFFER_TYPE_CHOICES = [
        (BASIC, 'Basic'),
        (STANDARD, 'Standard'),
        (PREMIUM, 'Premium'),
    ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details', default=None)
    title = models.CharField(max_length=200)
    revisions = models.IntegerField(default= -1)
    delivery_time_in_days = models.IntegerField(default=1)
    price = models.FloatField(default=0.00)
    features = models.JSONField(default=list) 
    offer_type = models.CharField(max_length=50, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.offer.title} - {self.title}"
