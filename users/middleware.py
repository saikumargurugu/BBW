from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from users.models import Users
import logging
from jwt.exceptions import ExpiredSignatureError

logger = logging.getLogger(__name__)

class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Always set a default user
        request.user = AnonymousUser()

        specific_public_paths = [
            "/api/auth/login/",
            "/api/auth/register/",
            "/api/user/layout_routes/",
            "/api/token/refresh/",
            "/api/user/signup/",
            "/api/user/forgot-password/",
        ]

        auth_header = request.headers.get("Authorization")
        print("================req path====================")
        print(f"Request path: {request.path}")
        print(f"Authorization header: {auth_header}")

        if not auth_header and auth_header is None:
            if request.path.startswith("/api/public") or request.path in specific_public_paths:
                print("================req path entered test====================")
                return None
            return JsonResponse({"error": "Unauthorized. Missing Authorization header."}, status=401)

        try:
            token = auth_header.split(" ")[1]
            print(f"Extracted token: {token}")
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            print(f"User ID from token: {user_id}")
            try:
                user = Users.objects.get(id=user_id)
                request.user = user
            except ExpiredSignatureError:
                print("Token has expired.")
                return JsonResponse({"error": "Unauthorized. Token has expired."}, status=401)
            except Users.DoesNotExist:
                return JsonResponse({"error": "Unauthorized. User does not exist."}, status=401)
        except Exception as e:
            print(f"Token verification failed: {str(e)}")
            return JsonResponse({"error": f"Unauthorized. Invalid token. {str(e)}"}, status=401)

        return None