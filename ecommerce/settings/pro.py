from .base import *

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

CELERY_BROKER_URL = 'redis://msrugs.com:6379'
CELERY_RESULT_BACKEND = 'redis://msrugs.com:6379'
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR3 / 'db.sqlite3',
#     }
# }