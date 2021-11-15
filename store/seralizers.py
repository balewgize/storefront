from decimal import Decimal
from rest_framework import serializers

from store.models import Cart, Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    """Serializer for Collection model."""

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
    """Serializer for Product model."""

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


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""

    class Meta:
        model = Review
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model."""

    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id"]
