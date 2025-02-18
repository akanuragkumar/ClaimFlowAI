import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claimflow.settings.local')

app = Celery("claimflow", broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"))

# Use Django settings to configure Celery
app.config_from_object("django.conf:settings", namespace="CELERY")

# Discover tasks from all registered Django app configs
app.autodiscover_tasks()

# Ensure Celery imports tasks from 'loss_run.tasks'
app.conf.imports = ('loss_run.tasks',)