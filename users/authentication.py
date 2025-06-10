from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
from users.models import Users  # Adjust import to your user model

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        id_token = auth_header.split(' ')[1]
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email')

            # Try to get the Django user by Firebase UID or email
            try:
                user = Users.objects.get(firebase_uid=uid)
            except Users.DoesNotExist:
                raise AuthenticationFailed("Firebase user has no email and does not exist in Django.")

            return (user, None)  # Return the Django user instance
        except Exception as e:
            raise AuthenticationFailed(f"Invalid Firebase token: {e}")