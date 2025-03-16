from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]
    
    offer_detail = models.ForeignKey(
        "offer_app.OfferDetail", 
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    customer_user = models.ForeignKey(User, related_name='customer_orders', on_delete=models.CASCADE)
    business_user = models.ForeignKey(User, related_name='business_orders', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    revisions = models.IntegerField(null=True, blank=True)
    delivery_time_in_days = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
