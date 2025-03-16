from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('business', 'Business')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    file = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=10, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil von {self.user.username}"
