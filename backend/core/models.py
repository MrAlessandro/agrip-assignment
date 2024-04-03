from ctypes import Array
from django import conf
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=127, unique=True)
    status = models.CharField(max_length=63)
    priority = models.CharField(max_length=63)
    section = models.CharField(max_length=63)
    installed_size = models.PositiveIntegerField()
    maintainer = models.CharField(max_length=255)
    original_maintainer = models.CharField(max_length=255)
    architecture = models.CharField(max_length=63)
    version = models.CharField(max_length=127)
    source = models.CharField(max_length=127, null=True)
    description = models.TextField()
    homepage = models.URLField(blank=True, null=True)
    python_version = models.CharField(max_length=127, null=True)
    provides = ArrayField(models.CharField(max_length=127), blank=True, null=True)
    replaces = ArrayField(models.CharField(max_length=127), blank=True, null=True)
    recommends = ArrayField(models.CharField(max_length=127), blank=True, null=True)

    def __str__(self):
        return self.name


class Dependency(models.Model):
    # this
    source = models.ForeignKey(
        Package, related_name="dependencies", on_delete=models.CASCADE
    )
    # depends on this
    target = models.ForeignKey(
        Package, related_name="reverse_dependencies", on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=100,
        choices=(
            ("depends", "Depends"),
            ("pre-depends", "Pre-Depends"),
        ),
    )

    def __str__(self):
        return f"{self.source.name} -> {self.target.name}"

    class Meta:
        unique_together = ("source", "target", "type")


class Conffile(models.Model):
    package = models.ForeignKey(
        Package, related_name="confiles", on_delete=models.CASCADE
    )
    path = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)

    def __str__(self):
        return self.path
