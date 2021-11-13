from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .seralizers import ProductSeralizer


@api_view()
def product_list(request):
    """Return the list of products in the store."""
    queryset = Product.objects.all()
    seralizer = ProductSeralizer(queryset, many=True)
    return Response(seralizer.data)


@api_view()
def product_detail(request, id):
    """Show the detail of selected product."""
    product = get_object_or_404(Product, pk=id)
    seralizer = ProductSeralizer(product)
    return Response(seralizer.data)
