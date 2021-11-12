from django.db.models.fields import DecimalField
from django.shortcuts import render
from django.db.models import F, Count, Value, ExpressionWrapper
from django.contrib.contenttypes.models import ContentType

from store.models import Customer, Order, OrderItem, Product
from tags.models import TaggedItem


def index(request):
    # Selecting all products that has been ordered
    # queryset = Product.objects.filter(
    #     id__in=OrderItem.objects.values("product_id").distinct()
    # )

    # Loading some fields later
    # queryset = Product.objects.defer("description")

    # select the last five orders with their customers and items (including product)
    # queryset = (
    #     Order.objects.select_related("customer")
    #     .prefetch_related("orderitem_set__product")
    #     .order_by("-placed_at")
    #     .all()[:5]
    # )

    # calling databse functions
    # queryset = Customer.objects.annotate(
    #     full_name=Concat("first_name", Value(" "), "last_name")
    # )

    # counting the number of orders by each customer
    # queryset = Customer.objects.annotate(total_orders=Count("order")).order_by(
    #     "-total_orders"
    # )

    # adding discounted_price as new field to products
    # discounted_price = ExpressionWrapper(
    #     F("unit_price") * 0.8, output_field=DecimalField(decimal_places=2)
    # )
    # queryset = Product.objects.annotate(discounted_price=discounted_price)

    # get all tags applied to a product with id=1
    tags = TaggedItem.objects.get_tags_for(Product, 1)

    # get products liked by the user
    # content_type = ContentType.objects.get_for_model(Product)
    # queryset = LikedItem.objects.select_related("user").filter(
    #     user=request.user, content_type=content_type, object_id=1
    # )

    context = {"tags": tags}
    return render(request, "index.html", context=context)
