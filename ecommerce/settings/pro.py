from .base import *

DEBUG = False

ADMINS = (
    ('EMRE','konakziyaemre@gmail.com'),
    )

ALLOWED_HOSTS = ['msrugs.com', '165.22.33.200', 'www.msrugs.com']

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