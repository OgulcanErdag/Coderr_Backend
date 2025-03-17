from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from authentication_app.models import UserProfile
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User
from authentication_app.models import UserProfile
from rest_framework.authtoken.models import Token

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=[('customer', 'Customer'), ('business', 'Business')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Die Passwörter stimmen nicht überein.")
        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user_type = validated_data.pop('type', None)

        if not user_type:
            raise serializers.ValidationError("Benutzertyp ist erforderlich.")

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)

            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user, type=user_type)
            else:
                print(f"UserProfile für {user.username} existiert bereits.")
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", required=False)
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    id = serializers.IntegerField(source="pk", read_only=True)

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.user.save()
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(read_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError(_("Ungültige Anmeldedaten"))
        data['user'] = user
        return data
    
