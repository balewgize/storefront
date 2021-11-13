from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def product_list(request):
    """Return the list of products in the store."""
    return Response("Okay, list of products")


@api_view()
def product_detail(request):
    """Show the detail of selected product."""
    return Response("The detail of one product.")
