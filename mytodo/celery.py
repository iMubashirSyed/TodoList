# Celery setup

from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','mytodo.settings')

app = Celery('mytodo', broker='redis://127.0.0.1:6379/0')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Karachi')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'send-due-task-reminders-every-day': {
        'task': 'todo.tasks.send_task_reminder',
        'schedule': crontab(minute='*'),  
    },
}

app.autodiscover_tasks()

@app.task(blind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')  
# app.conf.beat_schedule = {
#     'send-task-reminders': {
#         'task': 'todo.tasks.send_task_reminder',
#         'schedule': crontab(minute='*/5'),  # Runs every 5 minutes
#     },
# }