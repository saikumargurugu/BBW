from django.shortcuts import render

from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import random

from .models import Users
from .serializers import RegisterSerializer


class RegisterView(CreateModelMixin, GenericAPIView):
    """
    View to handle user registration using mixins.
    """
    queryset = Users.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        print('================================')
        print('File:',serializer )
        print('================================')
        if serializer.is_valid():
            user = serializer.save()

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Send OTP to user's email
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP code is {otp}. Please use this to verify your account.",
                from_email="your_email@example.com",  # Replace with your email
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "User registered successfully. OTP sent to email.", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(CreateModelMixin, GenericAPIView):
    """
    View to handle user login and return JWT tokens using mixins.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)