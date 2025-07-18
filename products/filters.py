from django_filters import rest_framework as filters
from .models import Items

class ItemFilter(filters.FilterSet):
    category_id = filters.NumberFilter(field_name='subcategory__category__id')
    category = filters.CharFilter(field_name='subcategory__category__name', lookup_expr='icontains')
    subcategory_id = filters.NumberFilter(field_name='subcategory__id')
    subcategory = filters.CharFilter(field_name='subcategory__name', lookup_expr='icontains')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = filters.BooleanFilter(field_name='is_available')

    class Meta:
        model = Items
        fields = []