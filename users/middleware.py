from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from firebase_admin import auth
from users.models import Users  # Import your custom Users model

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
        if not auth_header:
            return JsonResponse(
                {"error": "Unauthorized. Missing Authorization header."},
                status=401
            )

        # Extract the token from the Authorization header
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return JsonResponse(
                {"error": "Unauthorized. Invalid Authorization header format."},
                status=401
            )

        # Verify the token using Firebase Admin SDK
        try:
            decoded_token = auth.verify_id_token(token)
            email = decoded_token.get("email")

            # Fetch the user object from the database
            try:
                user = Users.objects.get(email=email)
                request.user = user  # Attach the user object to the request
            except Users.DoesNotExist:
                return JsonResponse(
                    {"error": "Unauthorized. User does not exist."},
                    status=401
                )
        except Exception as e:
            return JsonResponse(
                {"error": f"Unauthorized. Invalid token. {str(e)}"},
                status=401
            )

        return None