from celery import shared_task
from django.core.mail import send_mail, mail_admins
from django.template import loader
from django.conf import settings


