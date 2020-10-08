from .base import *


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'samnmdb',
#         'USER': 'emre',
#         'PASSWORD': 'Ziy@emre1992',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR3 / 'db.sqlite3',
    }
}