# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include, path
from rest_framework import routers
from django.conf import settings

from core.viewsets import PackageViewSet


router = routers.DefaultRouter()
router.register(r"packages", PackageViewSet, basename="package")

urlpatterns = [
    path("api/", include(router.urls)),
]
