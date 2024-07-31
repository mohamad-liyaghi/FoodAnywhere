from celery import Celery
from decouple import config

celery = Celery("config", broker=config("CELERY_BROKER_URL"))
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.config_defaults = {"broker_connection_retry_on_startup": True}


celery.autodiscover_tasks(["apps.core.tasks"])
