# Serializers define the API representation.
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Package


class PackageImportSerializer(ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"


class PackageDependencySerializer(ModelSerializer):
    class Meta:
        model = Package
        fields = [
            "id",
            "name",
        ]


class PackageListSerializer(ModelSerializer):
    dependencies = serializers.SerializerMethodField()

    def get_dependencies(self, obj):
        dependencies = obj.dependencies.select_related("target").all()
        return PackageDependencySerializer(
            [dep.target for dep in dependencies], many=True
        ).data

    class Meta:
        model = Package
        fields = [
            "id",
            "name",
            "description",
            "version",
            "dependencies",
        ]


class PackageSerializer(ModelSerializer):
    dependencies = serializers.SerializerMethodField()

    def get_dependencies(self, obj):
        dependencies = obj.dependencies.select_related("target").all()
        return PackageDependencySerializer(
            [dep.target for dep in dependencies], many=True
        ).data

    class Meta:
        model = Package
        fields = "__all__"
