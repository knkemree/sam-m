from .settings import *

DEBUG = False
ADMINS = (
    ('EMRE','konakziyaemre@gmail.com'),
)
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'samnm',
        'USER': 'postgres',
        'PASSWORD': 'Ziy@emre1992',
    }
}