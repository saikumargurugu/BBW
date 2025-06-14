from django.shortcuts import render
from rest_framework import generics
from shop.models import Product, Brand, ProductType, Category, SubCategory, Color
from shop.serializers import (
    ProductSerializer,
    BrandSerializer,
    ProductTypeSerializer,
    CategorySerializer,
    SubCategorySerializer,
    ColorSerializer,
)
from shop.pagination import ProductPagination

# List and Create API for Products
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

# Detail API for Products
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# List and Create API for Brands
class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# Detail API for Brands
class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# List and Create API for Categories
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Detail API for Categories
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
