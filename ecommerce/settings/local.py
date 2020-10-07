from .base import *

DEBUG = True


ADMINS = (
    ('EMRE','konakziyaemre@gmail.com'),
    )

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}