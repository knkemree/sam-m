from django.db import models

# Create your models here.
class Delivery_methods(models.Model):
    delivery_method = models.CharField(max_length=50, blank=True, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.delivery_method