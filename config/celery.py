# First steps with Django
# https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

from __future__ import absolute_import, unicode_literals
import datetime
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env.local')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)  # Cargar las variables de entorn

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(
    broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
@app.task
def reset_qr():
    from apps.accounts.models import User
    import secrets

    users = User.objects.all()
    for user in users:
      user.hash_qr = secrets.token_urlsafe()
      user.active_hash = True

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
