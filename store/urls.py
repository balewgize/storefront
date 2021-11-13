from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("products/", views.product_list, name="product-list"),
    path("product/1/", views.product_detail, name="product-detail"),
]
