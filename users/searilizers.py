from rest_framework import serializers
from .models import Users
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'password']

    def validate_password(self, value):
        return make_password(value)  # Hash the password before saving