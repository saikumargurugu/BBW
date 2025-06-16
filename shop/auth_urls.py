from django.urls import path
from shop.views import ProductCreateView, BrandCreateView

urlpatterns = [
    # ...other urls...
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('brands/create/', BrandCreateView.as_view(), name='brand-create'),
]