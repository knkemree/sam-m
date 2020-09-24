import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')


app = Celery('ecommerce')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)