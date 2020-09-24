from celery import task, shared_task
from django.core.mail import send_mail, mail_admins
from django.template import loader
from django.conf import settings
from .models import Order, OrderItem


@task
def order_created(order_id, html_message):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = "Order Confirmation - SAM&M Trade"
    message = "Thank you for your order!"
    mail_sent = send_mail(subject,message,
                        settings.DEFAULT_FROM_EMAIL, [order.email],
                        fail_silently=False,
                        html_message=html_message)
    return mail_sent

@task
def inform_admins(order_id, html_message):
    order = Order.objects.get(id=order_id)
    subject = "New Order - SAM&M Trade"
    message = str(order.company_name)+" placed an order!"

    mail_sent = mail_admins(subject, message, html_message=html_message)

    return mail_sent





@task(name="sum_two_numbers")
def add(x, y):
    return x + y


@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)
