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
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from .models import Users
from .serializers import RegisterSerializer


class FirebaseAuthView(GenericAPIView):
    def post(self, request):
        id_token = request.data.get("idToken")
        try:
            from firebase_admin import auth
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token["uid"]
            return Response({"message": "Authentication successful", "uid": uid})
        except Exception as e:
            return Response({"error": str(e)}, status=401)


class UserManagementView(CreateModelMixin, GenericAPIView):
    """
    View to handle user registration and deletion.
    """
    queryset = Users.objects.all()
    serializer_class = RegisterSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        """
        Register a new user.
        """
        # Generate a temporary password
        temp_password = get_random_string(length=8)

        # Add the temporary password to the request data
        request.data['password'] = temp_password

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the user in the database
            user = serializer.save()

            # Register the user in Firebase
            try:
                from firebase_admin import auth
                firebase_user = auth.create_user(
                    email=user.email,
                    password=temp_password,
                    display_name=user.username,
                )
                user.firebase_uid = firebase_user.uid  # Save Firebase UID in the database
                user.save()
                print(f"Firebase user created: {firebase_user.uid}")
            except Exception as e:
                print(f"Error creating Firebase user: {e}")
                return Response(
                    {"error": "Failed to register user in Firebase."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Send OTP or temporary password to the user's email
            send_mail(
                subject="Your Temporary Password",
                message=f"Your temporary password is {temp_password}. Please use this to log in.",
                from_email="your_email@example.com",  # Replace with your email
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "User registered successfully. Temporary password sent to email.", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Delete a user by ID.
        """
        user_id = kwargs.get('id')  # Retrieve the user ID from the URL parameters

        try:
            # Get the user from the Django database
            user = Users.objects.get(id=user_id)

            # Delete the user from Firebase
            try:
                from firebase_admin import auth
                auth.delete_user(user.firebase_uid)  # Assuming `firebase_uid` is stored in the Django user model
                print(f"Firebase user deleted: {user.firebase_uid}")
            except Exception as e:
                print(f"Error deleting Firebase user: {e}")
                return Response(
                    {"error": "Failed to delete user from Firebase."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Delete the user from the Django database
            user.delete()
            return Response(
                {"message": "User deleted successfully."},
                status=status.HTTP_200_OK,
            )
        except Users.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"Error deleting user: {e}")
            return Response(
                {"error": "Failed to delete user."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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