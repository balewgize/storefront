from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("products/", views.ProductList.as_view(), name="product-list"),
    path("product/<int:pk>/", views.ProductDetail.as_view(), name="product-detail"),
    path("collections/", views.CollectionList.as_view(), name="collection-list"),
    path(
        "collection/<int:pk>/",
        views.CollectionDetail.as_view(),
        name="collection-detail",
    ),
]
