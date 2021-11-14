from django.conf.urls import include
from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views


app_name = "store"

router = SimpleRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)


urlpatterns = [
    path("", include(router.urls)),
    # include any specific url pattern here
]
