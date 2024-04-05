import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dpkg_parser.settings.production")
app = Celery("dpkg_parser")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/1"),
        parse_dpkg_task.s(),
    )


@app.task(bind=True, ignore_result=True)
def parse_dpkg_task(*args, **kwargs):
    from django.core.cache import cache
    from django.conf import settings
    from core.parser import import_packages

    print("Parsing DPKG status file...")
    cache_last_modified = cache.get("dpkg_status_file_last_modified")
    file_last_modified = os.path.getmtime(settings.DPKG_STATUS_FILE)
    print(f"Cache last modified: {cache.get('dpkg_status_file_last_modified')}")
    if cache_last_modified is None or cache_last_modified < file_last_modified:
        print("Package repository is outdated. Parsing...")
        cache.set("dpkg_status_file_last_modified", file_last_modified)
        import_packages(settings.DPKG_STATUS_FILE)
