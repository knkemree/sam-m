from .base import *

DEBUG = Fasle

ALLOWED_HOSTS = ['165.22.33.200','msrugs.com','www.msrugs.com', 'www.samnmtrade.com', 'samnmtrade.com']
#ALLOWED_HOSTS = ['msrugs.com','www.msrugs.com']
INTERNAL_IPS = (
    '165.22.33.200',
)

def custom_show_toolbar(request):
    return True  # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,

}
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
AWS_DEFAULT_ACL = 'public-read'


STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CELERY_BROKER_URL='amqp://localhost'
CELERY_RESULT_BACKEND='amqp://localhost'

CKEDITOR_BASEPATH = "https://nyc3.digitaloceanspaces.com/samnm/samnm-static/ckeditor/ckeditor/"

