# users/urls.py
from django.urls import path
from users.views import LoginView,  UserManagementView, SignUpView, ForgotPasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # path('firebase/', FirebaseAuthView.as_view(), name='firebase_auth'),
    path('user/', UserManagementView.as_view(), name='user_management'),  # Combined view for register and delete
    path('signup/', SignUpView.as_view(), name='signup'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
]