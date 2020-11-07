from celery import shared_task
from django.core.mail import send_mail, mail_admins
from django.template import loader
from django.conf import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def inform_admin(email):
    
    subject = "New Customer Registered"
    message = "New Customer Registration! Customer's email address is "+str(email)

    mail_sent = mail_admins(subject, message,)

    return mail_sent