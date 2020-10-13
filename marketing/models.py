from django.db import models
import os

# Create your models here.
def slider_upload(instance, filename):
    return "slider/%s" %(filename)

class Slider(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d',default= 'img/no_image.png', blank=True, null=True)
    order = models.IntegerField(default=0)
    header_text = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['order','-start_date', '-end_date']