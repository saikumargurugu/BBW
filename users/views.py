from django.shortcuts import render

from rest_framework import generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from .models import Users
from .serializers import RegisterSerializer
import os  # Import os to access environment variables


class FirebaseAuthView(generics.GenericAPIView):
    def post(self, request):
        id_token = request.data.get("idToken")
        try:
            from firebase_admin import auth
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token["uid"]
            return Response({"message": "Authentication successful", "uid": uid})
        except Exception as e:
            return Response({"error": str(e)}, status=401)


class UserManagementView(mixins.CreateModelMixin, generics.GenericAPIView):
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

            # Register the user in Firebase
            try:
                user = serializer.save()
            except FirebaseError as e:
                if e.code == "EMAIL_EXISTS":
                    # Handle the case where the email already exists in Firebase
                    print(f"Firebase user already exists for email: {user.email}")
                    return Response(
                        {"error": "The email is already registered in Firebase."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
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


class SignUpView(mixins.CreateModelMixin, generics.GenericAPIView):
    """
    View to handle user registration using generic views and mixins.
    """
    queryset = Users.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle user registration.
        """
        # Generate a temporary password
        temp_password = get_random_string(length=8)

        # Add the temporary password to the request data
        request.data['password'] = temp_password

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            try:
                # Save the user in the database
                # Register the user in Firebase
                user = serializer.save()
            except Exception as e:
                print(f"Error creating Firebase user: {e}")
                return Response(
                    {"error": "Failed to register user in Firebase."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Get the sender email from environment variables
            from_email = os.getenv("FROM_EMAIL", "default_email@example.com")  # Default value if not set

            # Send OTP or temporary password to the user's email
            send_mail(
                subject="Your Temporary Password",
                message=f"Your temporary password is {temp_password}. Please use this to log in.",
                from_email=from_email,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "User registered successfully. Temporary password sent to email.", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)