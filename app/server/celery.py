from os import environ
from celery import Celery


# set the default Django settings module for the 'celery' program.
environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')


# configure celery app
app = Celery()
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """A debug celery task"""
    print(f'Request: {self.request!r}')
