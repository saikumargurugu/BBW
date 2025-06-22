from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views import ProductAdminViewSet  # This should be a ViewSet, not an APIView

router = DefaultRouter()
router.register(r'products', ProductAdminViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]