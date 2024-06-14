"""This module configures Celery for the Forum_V2 project."""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Forum_V2.settings')

app = Celery('Forum_V2')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'

app.conf.beat_schedule = {
    'send-daily-email-every-morning': {
        'task': 'qa_app.tasks.send_daily_email',
        'schedule': crontab(hour=8, minute=0),
    },
    "test-every-minute": {
        "task": "qa_app.tasks.test_task",
        "schedule": crontab(minute="*/1"),
    },
    'send-minute-email-every-minute': {
        'task': 'qa_app.tasks.send_minute_email',
        'schedule': crontab(minute='*/1'),
    },
    'save_visits_every-minute': {
        'task': 'qa_app.tasks.task_save_visits',
        'schedule': crontab(minute='*/1'),
    },
}
