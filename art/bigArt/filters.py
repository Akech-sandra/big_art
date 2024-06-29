import django_filters
from .models import Product

class ShopFilter(django_filters.FilterSet):
    product_name = django_filters.CharFilter(field_name='product_name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['product_name']