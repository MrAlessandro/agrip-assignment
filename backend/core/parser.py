from django.conf import settings

from core.models import Dependency, Package
from core.serializers import PackageImportSerializer


def parse_dependencies(dependencies_str):
    dependencies = []
    for dep in dependencies_str.split(", "):
        dep_name = dep.split(" ")[0]
        dependencies.append(dep_name)
    return dependencies


def parse_conffiles(conffiles_lines):
    conffiles = []
    for line in conffiles_lines:
        if line.strip():
            path, hash = line.split(" ", 1)
            conffiles.append({"path": path, "hash": hash.strip()})
        else:
            break
    return conffiles


def create_or_update_package(package_info, conffiles):
    package_serializer = PackageImportSerializer(data=package_info)
    package_serializer.is_valid()
    package, _ = Package.objects.update_or_create(
        name=package_info["name"],
        defaults=package_serializer.data,
    )

    dependencies = []
    for dep in set(package_info["depends"]):
        try:
            dep_package = Package.objects.get(name=dep)
            dependencies.append(
                Dependency(
                    source=package,
                    target=dep_package,
                    type="depends",
                )
            )
        except Package.DoesNotExist:
            pass

    for dep in set(package_info["pre_depends"]):
        try:
            dep_package = Package.objects.get(name=dep)
            dependencies.append(
                Dependency(
                    source=package,
                    target=dep_package,
                    type="pre_depends",
                )
            )
        except Package.DoesNotExist:
            pass

    return dependencies


def parse_package(package_str):
    package_lines = package_str.split("\n")
    package_info = {
        "depends": [],
        "pre_depends": [],
        "recommends": [],
        "replaces": [],
        "provides": [],
    }
    current_key = None

    for line in package_lines:
        if line.startswith(" "):
            package_info[current_key] += line
        else:
            current_key, current_value = line.split(":", 1)
            current_key = current_key.lower().replace("-", "_")
            current_value = current_value.strip()
            if line.startswith("Package:"):
                package_info["name"] = current_value
            elif (
                line.startswith("Depends:")
                or line.startswith("Pre-Depends:")
                or line.startswith("Recommends:")
                or line.startswith("Replaces:")
                or line.startswith("Provides:")
            ):
                package_info[current_key] = parse_dependencies(current_value)
            else:
                package_info[current_key] = current_value.strip()

    return create_or_update_package(package_info, [])


def import_packages(file_path):
    with open(file_path, "r") as file:
        package_data = file.read()

    packages = package_data.split("\n\n")
    dependencies = []
    for package in packages:
        if package:
            dep = parse_package(package)
            dependencies += dep
    Dependency.objects.all().delete()
    Dependency.objects.bulk_create(dependencies)
