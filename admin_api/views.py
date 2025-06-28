from rest_framework import viewsets
from rest_framework import generics
from shop.models import Product, Brand, ProductType, Category, Color, ProductImage
from users.permissions import IsAdminUser  
from shop.serializers import (
    ProductSerializer,
    BrandSerializer,
    ProductTypeSerializer,
    ColorSerializer,
    CategorySerializer,
    ProductAdminListSerializer,
    ProductAdminDetailSerializer,
)
from shop.pagination import ProductPagination
from rest_framework import status
from rest_framework.response import Response

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from utils.utils import handle_file_upload
from django.conf import settings
from rest_framework.decorators import action

# Create your views here.

# Create API for Products (separate endpoint, if needed)
#  ADMIN APIS for Product Creation

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser] 


class ProductAdminViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductAdminListSerializer
    pagination_class = ProductPagination
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductAdminDetailSerializer
        return ProductAdminListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        # Handle images if provided
        images = request.data.get('images', [])
        if isinstance(images, str):
            import json
            images = json.loads(images)
        for img_url in images:
            ProductImage.objects.create(product=product, image_url=img_url)
        return Response(self.get_serializer(product).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        # Handle images update
        images = request.data.get('images', [])
        if isinstance(images, str):
            import json
            images = json.loads(images)
        # Remove old images
        ProductImage.objects.filter(product=product).delete()
        # Add new images
        for img_url in images:
            ProductImage.objects.create(product=product, image_url=img_url)
        return Response(self.get_serializer(product).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Delete related images
        ProductImage.objects.filter(product=instance).delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='uploads', parser_classes=[MultiPartParser, FormParser])
    def uploads(self, request, pk=None):
        print("Update request data:", request.data)
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        if pk == 'new' or pk is None:
            url = 'products/draft/images/'
        else:
            url = f"products/{pk}/images/"
        upload = handle_file_upload(file_obj, model_name='Product', url=url)

        return Response({
            'id': upload.id,
            'unique_id': upload.unique_id,
            'path': upload.path,
            'model': upload.model,
            'file_size': upload.file_size,
            'type': upload.file_type,
            'url': f"{settings.MEDIA_URL}{upload.path}",
            'object_id': pk
        }, status=status.HTTP_201_CREATED)

class BrandAdminViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        return BrandSerializer

class CategoryAdminViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        return CategorySerializer

class ProductTypeAdminViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        return ProductTypeSerializer

class ColorAdminViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        return ColorSerializer


# class FileUploadView(viewsets.ModelViewSet):
#     parser_classes = (MultiPartParser, FormParser)
#     permission_classes = [IsAdminUser]

#     def post(self, request, *args, **kwargs):
#         file_obj = request.FILES.get('file')
#         if not file_obj:
#             return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
#         obj_id = kwargs.get('id')
#         model =  'Product'
#         url = f"products/{obj_id}/images/" if obj_id else None
#         upload = handle_file_upload(file_obj, model, url)

#         return Response({
#             'id': upload.id,
#             'unique_id': upload.unique_id,
#             'path': upload.path,
#             'model': upload.model,
#             'file_size': upload.file_size,
#             'type': upload.type,
#             'url': f"{settings.MEDIA_URL}{upload.path}",
#             'object_id': obj_id
#         }, status=status.HTTP_201_CREATED)


