from django.db import models
from ckeditor.fields import RichTextField  # Import RichTextField from django-ckeditor

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Optional discount

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Optional discount

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Optional discount

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subcategories = models.ManyToManyField(SubCategory, related_name="categories")
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Optional discount

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name="products", null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, related_name="products", null=True)
    colors = models.ManyToManyField(Color, related_name="products")  
    qty = models.PositiveIntegerField(default=0) 
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    product_details = RichTextField()  # Use RichTextField for formatted text
    in_stock = models.BooleanField(default=True) 
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) 

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(max_length=500)

    def __str__(self):
        return f"Image for {self.product.name}"
