from rest_framework import serializers
from shop.models import Product, Brand, ProductType, Category, Color

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    product_type = ProductTypeSerializer(read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        extra_fields = ['url']

    def get_url(self, obj):
        return f"/shop/products/{obj.id}/details"

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color  # Change this to your ProductImage model if you have one
        fields = ['id', 'image_url']

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    brand = serializers.CharField(source='brand.name', read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'images',
            'description',
            'brand',
            'stock',
            'url',
        ]

    def get_url(self, obj):
        return f"/shop/products/{obj.id}/details"
    






    # ADMMIN SERIALIZERS


class ProductAdminListSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    product_type_name = serializers.CharField(source='product_type.name', read_only=True)
    color_names = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'brand_name',
            'product_type_name',
            'color_names',
            'url',
        ]

    def get_color_names(self, obj):
        return [color.name for color in obj.colors.all()]

    def get_url(self, obj):
        return f"/products/{obj.id}/details"

class ProductAdminDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    product_type = ProductTypeSerializer(read_only=True)
    colors = ColorSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'brand',
            'category',
            'product_type',
            'colors',
            'qty',
            'price',
            'product_details',
            'in_stock',
            'discount',
            # add any other fields you want to expose
        ]
