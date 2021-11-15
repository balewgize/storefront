from django_filters import rest_framework as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    """Custom filter for product model."""

    class Meta:
        model = Product
        fields = {"collection_id": ["exact"], "unit_price": ["gte", "lte"]}
