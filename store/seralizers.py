from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models.aggregates import Sum
from rest_framework import serializers
from rest_framework.utils import field_mapping

from store.models import Cart, CartItem, Customer, Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    """Serializer for Collection model."""

    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

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


class SimpleProductSerializer(serializers.ModelSerializer):
    """Expose few informaion about a product."""

    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""

    class Meta:
        model = Review
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem model."""

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]

    def get_total_price(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model."""

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]

    def get_total_price(self, cart: Cart):
        return sum(
            [item.quantity * item.product.unit_price for item in cart.items.all()]
        )


class AddCartItemSerializer(serializers.ModelSerializer):
    """Custom Serializer for adding items to a cart."""

    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise ValidationError("No Product with the given ID was found.")
        return value

    def save(self, **kwargs):
        # get the cart_id from the context passed by CartItemViewSet
        cart_id = self.context["cart_id"]
        # get product_id and quantity from the POST request data
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    """Custom serializer to update a cart item."""

    class Meta:
        model = CartItem
        fields = ["quantity"]


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for the customer model."""

    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]
