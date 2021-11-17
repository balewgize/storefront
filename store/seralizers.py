from django.db import transaction
from rest_framework import serializers

from store.models import *


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
            raise serializers.ValidationError("No Product with the given ID was found.")
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


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for the OrderItem model."""

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "total_price"]

    def get_total_price(self, order_item):
        return order_item.quantity * order_item.product.unit_price


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model."""

    customer_id = serializers.IntegerField(read_only=True)
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_id",
            "placed_at",
            "payment_status",
            "items",
            "total_price",
        ]

    def get_total_price(self, order):
        return sum(
            [item.quantity * item.product.unit_price for item in order.items.all()]
        )


class UpdateOrderSerializer(serializers.ModelSerializer):
    """Serializer to update the payment status of an order."""

    class Meta:
        model = Order
        fields = ["payment_status"]


class CreateOrderSerializer(serializers.Serializer):
    """Custom serializer to create an order."""

    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("No cart with the given ID was found.")
        elif CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError(
                "The cart is empty. Please add one or more products."
            )
        return cart_id

    def save(self, **kwargs):
        # we need to get cart items and convert them to order items
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            customer, created = Customer.objects.get_or_create(
                user_id=self.context["user_id"]
            )
            order = Order.objects.create(customer=customer)

            # get cart items from the POST request
            cart_items = CartItem.objects.select_related("product").filter(
                cart_id=cart_id
            )
            # convert cart items to order items
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity,
                )
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            # finally remove the cart object
            Cart.objects.filter(pk=cart_id).delete()

            return order
