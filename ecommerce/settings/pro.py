from .base import *

DEBUG = True

ADMINS = (
    ('EMRE','konakziyaemre@gmail.com'),
    )

ALLOWED_HOSTS = ['msrugs.com', '165.22.33.200', 'www.msrugs.com','127.0.0.1','127.0.0.0']

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