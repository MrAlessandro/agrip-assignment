import os
from django.core.management.base import BaseCommand, CommandError
from core.parser import import_packages


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "status_file_path",
            type=str,
        )

    def handle(self, *args, **options):
        status_file_path = options["status_file_path"]
        if not os.path.exists(status_file_path):
            raise CommandError(f"The file {status_file_path} does not exist")

        import_packages(status_file_path)
