# First steps with Django
# https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

from __future__ import absolute_import
import datetime
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
# from apps.students.tasks import status
# from apps.students.models import studentList
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env.local')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)  # Cargar las variables de entorn
# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings",namespace='CELERY')

app = Celery(
    'config',
    broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(settings.INSTALLED_APPS)

if __name__ == "__main__":
    app.start()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, print_status, name='Imp status 10s')

    # # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
         crontab(minute=0, hour=0)
    )

@app.task
def status():
    from apps.students.models import studentList
    students = studentList.objects.all()
    for std in students:
        std.status = "AVAILABLE"
        std.save()
        print(f"change: {std.student.first_name} {std.status}")

@app.task
def reset_reko():
    from apps.family.models import Family, replacement
    tutors = Family.objects.all()
    replcs = replacement.objects.all()
    for tutor in tutors:
        tutor.canUseReko = True
        tutor.counterReko = 3
        tutor.timeReko = None
        tutor.save()
    for replc in replcs:
        replc.canUseReko = True
        replc.counterReko = 3
        replc.timeReko = None
        replc.save()

@app.task
def reset_qr():
    from apps.accounts.models import User
    import secrets

    users = User.objects.all()
    for user in users:
      user.hash_qr = secrets.token_urlsafe()
      user.active_hash = True

@app.task
def print_status():
    from apps.students.models import studentList
    students = studentList.objects.all()
    for std in students:
        print(f"{std.student.first_name} {std.status} {datetime.datetime.now()}")
