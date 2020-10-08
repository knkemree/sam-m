from .base import *

DEBUG = True


ADMINS = (
    ('EMRE','konakziyaemre@gmail.com'),
    )



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR3 / 'db.sqlite3',
    }
}