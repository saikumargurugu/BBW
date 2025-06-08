from django.urls import path
from shop.views import (
    ProductListCreateView,
    ProductDetailView,
    BrandListCreateView,
    BrandDetailView,
    CategoryListCreateView,
    CategoryDetailView,
)

urlpatterns = [
    # Product APIs
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Brand APIs
    path('brands/', BrandListCreateView.as_view(), name='brand-list-create'),
    path('brands/<int:pk>/', BrandDetailView.as_view(), name='brand-detail'),

    # Category APIs
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]