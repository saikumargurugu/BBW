from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Users, UserAddress, Router
from .serializers import RegisterSerializer, UserSerializer  # Import the serializer for the user object
import os  # Import os to access environment variables
from rest_framework.views import APIView


Users = get_user_model()


# class FirebaseAuthView(generics.GenericAPIView):
#     def post(self, request):
#         id_token = request.data.get("idToken")
#         try:
#             from firebase_admin import auth
#             decoded_token = auth.verify_id_token(id_token)
#             uid = decoded_token["uid"]
#             return Response({"message": "Authentication successful", "uid": uid})
#         except Exception as e:
#             return Response({"error": str(e)}, status=401)


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
                from_email= os.getenv("FROM_EMAIL", "default_email@example.com"),  # Replace with your email
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


class LoginView(APIView):
    """
    View to handle user login using Firebase ID tokens and return JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        id_token = request.data.get("idToken")
        print(f"Received ID token: {id_token}")  # Debugging log
        if not id_token:
            return Response(
                {"error": "ID token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Verify the Firebase ID token
            decoded_token = auth.verify_id_token(id_token)
            print(f"Decoded Firebase token: {decoded_token}")  # Debugging log

            email = decoded_token.get("email")
            print(f"Decoded email: {email}")  # Debugging log
            if not email:
                return Response(
                    {"error": "Invalid token. Email claim is missing."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Check if the user exists in the database
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                return Response(
                    {"error": "User does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)

            # Serialize the user object
            user_data = UserSerializer(user).data

            return Response(
                {
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": user_data,
                },
                status=status.HTTP_200_OK,
            )
        except FirebaseError as e:
            print(f"Firebase error: {e}")  # Debugging log
            return Response(
                {"error": f"Invalid ID token. {str(e)}"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            print(f"Unexpected error: {e}")  # Debugging log
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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
                user = serializer.save()

                # Extract address details from the request
                address_data = request.data.get("address", {})
                street = address_data.get("street", "Default Street")
                city = address_data.get("city", "Default City")
                state = address_data.get("state", "Default State")
                country = address_data.get("country", "Default Country")
                postal_code = address_data.get("postal_code", "000000")
                is_home = address_data.get("is_home", True)
                is_postal = address_data.get("is_postal", True)

                # Create a UserAddress instance
                UserAddress.objects.create(
                    user=user,
                    street=street,
                    city=city,
                    state=state,
                    country=country,
                    postal_code=postal_code,
                    is_home=is_home,
                    is_postal=is_postal,
                )

                # Send OTP or temporary password to the user's email
                from_email = os.getenv("FROM_EMAIL", "default_email@example.com")
                send_mail(
                    subject="Your Temporary Password",
                    message=f"Your temporary password is {temp_password}. Please use this to log in.",
                    from_email=from_email,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                # Return a 200 OK response
                return Response(
                    {"message": "User registered successfully. Temporary password sent to email.", "user_id": user.id},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                print(f"Error creating user: {e}")
                return Response(
                    {"error": "Failed to register user."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        # If serializer is not valid, return a 400 Bad Request response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    """
    API to handle forgot password functionality by sending a password reset email via Firebase.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle forgot password requests.
        """
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Check if the user exists in the database
            if not Users.objects.filter(email=email).exists():
                return Response(
                    {"error": "User with this email does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Generate the password reset link using Firebase
            reset_link = auth.generate_password_reset_link(email)

            # Render the HTML email template
            subject = "Reset Your Password"
            from_email = os.getenv("FROM_EMAIL", "default_email@example.com")
            context = {
                "reset_link": reset_link,
                "email": email,
            }
            html_content = render_to_string("emails/reset_password.html", context)
            text_content = f"Click the link below to reset your password:\n\n{reset_link}"

            # Send the email
            email_message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[email],
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            return Response(
                {"message": "Password reset email sent successfully."},
                status=status.HTTP_200_OK,
            )
        except FirebaseError as e:
            print(f"Firebase error: {e}")
            return Response(
                {"error": "Failed to send password reset email. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            print(f"Error: {e}")
            return Response(
                {"error": "An unexpected error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LayoutPropsView(APIView):
    """
    API to return navigation links and footer text using the Router model.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        
        if request.user.is_anonymous:
            # If the user is not authenticated, set is_authenticated to False
            user_is_authenticated = False
        else:
            user_is_authenticated = getattr(request.user, "is_authenticated", False)

        if user_is_authenticated:
            routers = Router.objects.filter(is_auth_route=True).order_by('id')
        else:
            routers = Router.objects.filter(is_auth_route=False).order_by('id')

        nav_links = [
            {"label": router.label, "href": router.url}
            for router in routers
        ]
        layOutProps = {
            "navLinks": nav_links,
            "fotterText": "© 2025 Badminton Association. All rights reserved.",
        }
        return Response(layOutProps)
