# users/urls.py
from django.urls import path
from users.views import LoginView, UserManagementView, LayoutPropsView, SignUpView, ForgotPasswordView

urlpatterns = [
    path('', UserManagementView.as_view(), name='user_management'),
    path("layout_routes/", LayoutPropsView.as_view(), name="layout_routes"),
    ]