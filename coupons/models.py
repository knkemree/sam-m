from django.db import models
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
class Coupon(models.Model):
    code = models.CharField(max_length=50,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
                   validators=[MinValueValidator(0),
                               MaxValueValidator(100)])
    active = models.BooleanField()
    def __str__(self):
        return self.code


class Campaign(models.Model):
    campaign_name = models.CharField(max_length=50,
                            unique=True)
    amount_from = models.PositiveIntegerField(unique=True, help_text="bigger than or equals to")
    amount_to = models.PositiveIntegerField(unique=True, help_text="bigger than or equals to")
    campaign_discount = models.IntegerField(
                   validators=[MinValueValidator(0),
                               MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.campaign_name


    
        