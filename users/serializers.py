# users/serializers.py
from rest_framework import serializers
from .models import Users  # Use your custom Users model
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users  # Use your custom Users model
        fields = ['username', 'email', 'password', 'phone', 'orgnisations']  # Include custom fields

    def create(self, validated_data):
        # Remove 'orgnisations' from validated_data
        orgnisations = validated_data.pop('orgnisations', [])
        
        # Create the user instance
        validated_data['password'] = make_password(validated_data['password'])  # Hash the password
        user = Users.objects.create(**validated_data)
        
        # Add organisations to the user
        user.orgnisations.set(orgnisations)
        
        return user
    