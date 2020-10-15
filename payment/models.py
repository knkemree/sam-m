from django.db import models
from django.db.models.signals import post_save
from account.models import Customers

# Create your models here.
class BillingProfile(models.Model):
    email = models.OneToOneField(Customers, null=True, blank=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    #customer_ id  = strpe or braintree

    def __str__(self):
        return self.email.email

# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print(" send to stripe")
#         instance.customer_id = newID
#         instance.save()

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(email=instance)

post_save.connect(user_created_receiver, sender=Customers)


    