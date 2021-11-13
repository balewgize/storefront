from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("products/", views.product_list, name="product-list"),
    path("product/<int:id>/", views.product_detail, name="product-detail"),
    path("collections/", views.collection_list, name="collection-list"),
    path("collection/<int:pk>/", views.collection_detail, name="collection-detail"),
]
