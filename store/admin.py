from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.messages.constants import SUCCESS
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html

from tags.models import Tag, TaggedItem


from . import models


class InventoryFilter(admin.SimpleListFilter):
    """Custom filter used to filter products based on their inventory."""

    title = "inventory"  # displayed as: By 'title'
    parameter_name = "inventory"  # parameter name used in the URL

    def lookups(self, request, model_admin):
        return [("low", "Low")]

    def queryset(self, request, queryset):
        if self.value() == "low":
            return queryset.filter(inventory__lt=10)


class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ["tag"]
    extra = 0


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    """Custom admin for managing Products."""

    actions = ["clear_inventory"]
    autocomplete_fields = ["collection"]
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_filter = ["collection", "last_update", InventoryFilter]
    list_per_page = 10
    list_select_related = ["collection"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ["title"]}
    inlines = [TagInline]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        return "Low" if product.inventory < 10 else "Ok"

    def collection_title(self, product):
        return product.collection.title

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        """A custom action used to clear inventory of a product."""
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated.",
            messages.SUCCESS,
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Custom admin for managing Customers"""

    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    list_per_page = 10
    list_filter = ["membership"]
    ordering = ["first_name", "last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    def orders_count(self, customer):
        # we the order count is clicked, display the list of orders by the customer
        url = (
            reverse("admin:store_order_changelist")
            + "?customer__id="
            + str(customer.id)
        )
        return format_html("<a href={}>{}</a", url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ["product"]
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """Custom admin for managing Orders."""

    autocomplete_fields = ["customer"]
    list_display = ["id", "placed_at", "payment_status", "customer"]
    list_per_page = 10
    list_select_related = ["customer"]
    list_filter = ["placed_at", "payment_status"]
    inlines = [OrderItemInline]


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    """Custom admin for managing Collections."""

    list_display = ["title", "products_count"]
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        # when count is clicked, display list of products in that collection
        # we need to get the url of product list page -- admin:app_model_page
        url = (
            reverse("admin:store_product_changelist")
            + "?collection__id__exact="
            + str(collection.id)
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("product"))
