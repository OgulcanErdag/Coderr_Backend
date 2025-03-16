from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Review(models.Model):
    business_user = models.ForeignKey(User, related_name="business_reviews", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name="reviewer_reviews", on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def update(self, **kwargs):
        updated_at = now()
        super().save(**kwargs)

    def __str__(self):
        return f"{self.reviewer} reviewed {self.business_user}"

