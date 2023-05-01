import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

app = Celery("task_manager")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "every": {
        "task": "tasks.tasks.check_expired",
        "schedule": crontab(),  # по умолчанию выполняет каждую минуту, очень гибко
    },  # настраивается
    "check_deadline": {
        "task": "tasks.tasks.check_deadline",
        "schedule": crontab(),  # по умолчанию выполняет каждую минуту, очень гибко
    },  # настраивается
    "check_expired" : {
        "task": "accounts.tasks.check_expired",
        "schedule": crontab(),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
