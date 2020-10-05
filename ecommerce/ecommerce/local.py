from .settings import *
DEBUG = True
ALLOWED_HOSTS = []
ADMINS = (('EMRE','konakziyaemre@gmail.com'),)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'samnm',
        'USER': 'postgres',
        'PASSWORD': 'Ziy@emre1992',
    }
}


