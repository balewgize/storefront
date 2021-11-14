from decimal import Decimal
from rest_framework import serializers

from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    # to include products_count additonal field which is not in the model
    # we have to options: annotaion and serializer method field
    # products_count = serializers.SerializerMethodField(method_name="count_products")

    # # return number of products in the collection
    # def count_products(self, collection):
    #     return collection.product_set.count()

    # # using annotation: annotate products_count when querying collecion
    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    """Convert a Product model to a python dictionary to return as a JSON."""

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "unit_price",
            "inventory",
            "collection",
            "slug",
        ]

    # price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    # # collection = serializers.PrimaryKeyRelatedField() # primary key
    # # collection = serializers.StringRelatedField() # String
    # collection = CollectionSeralizer()  # nested objects
    # collection = serializers.HyperlinkedRelatedField(
    #     view_name="store:collection-detail", queryset=Collection.objects.all()
    # )

    # def calculate_tax(self, product: Product):
    #     return product.unit_price * Decimal(1.1)

    # # to modify the object before creating: override create() method
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other_filed = "some value"
    #     product.save()
    #     return product

    # # to modify an object before updating: override the update() method
    # def update(self, instance, validated_data):
    #     instance.field_name = "some value"
    #     instance.save()
    #     return instance
