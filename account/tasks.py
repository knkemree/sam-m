from celery import shared_task
from django.core.mail import send_mail, mail_admins
from django.template import loader
from django.conf import settings


@shared_task
def info_admins(email):
    subject = "New Customer - SAM&M Trade"
    message = str(email)+" placed an order!"

    mail_sent = mail_admins(subject, message, html_message=email)

    return mail_sent