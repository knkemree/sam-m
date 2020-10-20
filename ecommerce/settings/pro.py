from .base import *

DEBUG = True

ALLOWED_HOSTS = ['165.22.33.200','msrugs.com','www.msrugs.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'samnmdb',
        'USER': 'emre',
        'PASSWORD': 'Ziy@emre1992',
        'HOST': 'localhost',
        'PORT': '',
    }
}

#STATIC_ROOT = "/var/www/msrugs.com/static/"

CELERY_BROKER_URL='redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND='redis://127.0.0.1:6379'
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR3 / 'db.sqlite3',
#     }
# }