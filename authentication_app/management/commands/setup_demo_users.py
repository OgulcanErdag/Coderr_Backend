from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = "Legt Demo-User (Gast-Login) für Anbieter und Kunde an."

    def handle(self, *args, **kwargs):
        demo_users = [
            {
                "username": "andrey",
                "email": "andrey@demo.com",
                "password": "asdasd",
                "type": "customer"
            },
            {
                "username": "kevin",
                "email": "kevin@demo.com",
                "password": "asdasd24",
                "type": "business"
            }
        ]

        for user_data in demo_users:
            username = user_data["username"]
            email = user_data["email"]
            password = user_data["password"]
            user_type = user_data["type"]

            user, created = User.objects.get_or_create(username=username, defaults={"email": email})
            if created:
                user.set_password(password)
                user.is_active = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Benutzer '{username}' erstellt."))
            else:
                self.stdout.write(self.style.WARNING(f"Benutzer '{username}' existiert bereits."))

            Token.objects.get_or_create(user=user)

            profile, profile_created = UserProfile.objects.get_or_create(user=user, defaults={"type": user_type})
            if profile_created:
                self.stdout.write(self.style.SUCCESS(f" Profil für '{username}' erstellt als '{user_type}'."))
            else:
                self.stdout.write(self.style.WARNING(f" Profil für '{username}' existiert bereits."))
