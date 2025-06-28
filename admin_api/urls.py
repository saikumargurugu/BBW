from django.urls import path, include
from rest_framework.routers import DefaultRouter
from admin_api.views import (
    ProductAdminViewSet,
    BrandAdminViewSet,
    CategoryAdminViewSet,
    ColorAdminViewSet,
    ProductTypeAdminViewSet,
    # FileUploadView,
)

router = DefaultRouter()
router.register(r'products', ProductAdminViewSet, basename='admin_products')
router.register(r'brands', BrandAdminViewSet, basename='admin_brands')
router.register(r'categories', CategoryAdminViewSet, basename='admin_categories')
router.register(r'product-types', ProductTypeAdminViewSet, basename='admin_product-types')
router.register(r'colors', ColorAdminViewSet, basename='admin_colors')


urlpatterns = [
    path('', include(router.urls)),
]   