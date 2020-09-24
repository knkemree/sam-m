from django.db import models

# Create your models here.
class Delivery_methods(models.Model):
    delivery_method = models.CharField(max_length=50, blank=True, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta: 
        ordering = ('delivery_method',) 
        verbose_name = 'Delivery Method' 
        verbose_name_plural = 'Delivery Methods'

    def __str__(self):
        return self.delivery_method

     