from django.shortcuts import render
from rest_framework import generics
from shop.models import Product, Brand, ProductType, Category, SubCategory, Color
from users.permissions import IsAdminUser  
from shop.serializers import (
    ProductSerializer,
    BrandSerializer,
    ProductTypeSerializer,
    CategorySerializer,
    SubCategorySerializer,
    ColorSerializer,
    ProductDetailSerializer,  # if you want to use it for detail
)
from shop.pagination import ProductPagination

# List and Create API for Products
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

# Create API for Products (separate endpoint, if needed)
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]  # Assuming you have a custom permission class for admin users

# Detail API for Products
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # or ProductDetailSerializer

# List and Create API for Brands
class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# Create API for Brands (separate endpoint, if needed)
class BrandCreateView(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser] 

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
