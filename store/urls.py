from django.urls import path, include
from rest_framework_nested import routers

from . import views


app_name = "store"

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet, basename="collections")

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls))
    # include any specific url pattern here
]