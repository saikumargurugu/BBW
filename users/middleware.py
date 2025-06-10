from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from users.models import Users  # Import your custom Users model
import logging

logger = logging.getLogger(__name__)

class AuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate API calls and add the user object to the request.
    Public APIs are bypassed.
    """

    def process_request(self, request):
        # Define specific public API paths that don't require authentication
        specific_public_paths = [
            "/api/auth/login/",
            "/api/auth/register/",
        ]

        # Check if the request path is a public API
        if request.path.startswith("/api/public/") or request.path in specific_public_paths:
            return None  # Bypass authentication for public APIs

        # Get the Authorization header
        auth_header = request.headers.get("Authorization")
        print(f"Authorization header: {auth_header}")
        if not auth_header:
            return JsonResponse({"error": "Unauthorized. Missing Authorization header."}, status=401)

        try:
            # Extract the token from the Authorization header
            token = auth_header.split(" ")[1]
            print(f"Extracted token: {token}")
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            print(f"User ID from token: {user_id}")

            # Fetch the user object from the database
            try:
                user = Users.objects.get(id=user_id)
                request.user = user
            except Users.DoesNotExist:
                return JsonResponse({"error": "Unauthorized. User does not exist."}, status=401)
        except Exception as e:
            print(f"Token verification failed: {str(e)}")
            return JsonResponse({"error": f"Unauthorized. Invalid token. {str(e)}"}, status=401)

        return None
    




    """
    from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from firebase_admin import auth
from users.models import Users  # Import your custom Users model
import logging
import jwt

logger = logging.getLogger(__name__)

class AuthenticationMiddleware(MiddlewareMixin):
    """
    # Middleware to authenticate API calls and add the user object to the request.
    # Public APIs are bypassed.
    """

    def process_request(self, request):
        # Define specific public API paths that don't require authentication
        specific_public_paths = [
            "/api/auth/login/",
            "/api/auth/register/",
        ]

        # Check if the request path is a public API
        if request.path.startswith("/api/public/") or request.path in specific_public_paths:
            return None  # Bypass authentication for public APIs

        # Get the Authorization header
        auth_header = request.headers.get("Authorization")
        print(f"Authorization header: {auth_header}")
        if not auth_header:
            return JsonResponse({"error": "Unauthorized. Missing Authorization header."}, status=401)

        try:
            # Extract the token from the Authorization header
            token = auth_header.split(" ")[1]
            print(f"Extracted token: {token}")
            # Verify the token using Firebase Admin SDK
            decoded_token2 = jwt.decode(token, options={"verify_signature": False})
            print(f"Decoded token2: {decoded_token2}")
            decoded_token = auth.verify_id_token(token)
            print(f"Decoded token: {decoded_token}")
            email = decoded_token2.get("email")
            print(f"Email from token: {email}")
            if not email:
                return JsonResponse({"error": "Invalid token. Email claim is missing."}, status=401)

            # Fetch the user object from the database
            try:
                user = Users.objects.get(email=email)
                request.user = user  # Attach the user object to the request
            except Users.DoesNotExist:
                return JsonResponse({"error": "Unauthorized. User does not exist."}, status=401)
        except Exception as e:
            print(f"Token verification failed: {str(e)}")
            return JsonResponse({"error": f"Unauthorized. Invalid token. {str(e)}"}, status=401)

        return None
    """