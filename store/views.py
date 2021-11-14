from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Collection, Product
from .seralizers import CollectionSerializer, ProductSerializer


class ProductList(APIView):
    """End point for all products and creating new product."""

    def get(self, request):
        queryset = Product.objects.select_related("collection").all()[:5]
        serializer = ProductSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    """End point for a single product."""

    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            # this product is associated with some orders, so can't be deleted
            return Response(
                {
                    "error": "Product cannot be deleted because it is associated with an order item."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
    """End point for a list of collections and creating a single collection."""

    def get(self, request):
        queryset = Collection.objects.annotate(products_count=Count("product")).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):
    """End point for a single collection."""

    def get(self, request, id):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count("product")), pk=id
        )
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def put(self, request, id):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count("product")), pk=id
        )
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count("product")), pk=id
        )
        if collection.product_set.count() > 0:
            return Response(
                {
                    "error": "Collection cannot be delete because it contains one or more products."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
