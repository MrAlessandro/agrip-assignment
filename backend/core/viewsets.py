from rest_framework import permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from core.models import Package
from core.serializers import PackageListSerializer, PackageSerializer


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.prefetch_related("dependencies__target").all()
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 20

    def get_serializer_class(self):
        if self.action == "list":
            return PackageListSerializer
        else:
            return PackageSerializer
