from django.utils.deprecation import MiddlewareMixin

class CustomJWTMiddleware(MiddlewareMixin):
    """
    Middleware to process requests and responses for JWT authentication.
    """
    def process_request(self, request):
        # Example: Add custom logic for incoming requests
        print(f"Request Method: {request.method}, Request Path: {request.path}")
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            print(f"JWT Token: {token}")
        return None

    def process_response(self, request, response):
        # Example: Add custom logic for outgoing responses
        response['X-Custom-Header'] = 'CustomJWTMiddleware'
        return response