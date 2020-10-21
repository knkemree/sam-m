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

AWS_ACCESS_KEY_ID = '7E2P4RU72GNS5Z4USMPC'
AWS_SECRET_ACCESS_KEY = 'G22GYFbv1Yjkp/5malq7BeUWGUSVV4MU4NYdwlRJlCk'
AWS_STORAGE_BUCKET_NAME = 'samnm'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'samnm-static'


STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CELERY_BROKER_URL='redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND='redis://127.0.0.1:6379'

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-csrf-token',
]

CORS_ORIGIN_ALLOW_ALL=True

CORS_ORIGIN_WHITELIST = [
    "https://msrugs.com",
]