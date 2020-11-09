from django.db import models
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from PIL import Image

# Create your models here.
def slider_upload(instance, filename):
    return "slider/%s" %(filename)

class Slider(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d',default= 'img/no_image.png', blank=True, null=True)
    order = models.IntegerField(default=0)
    header_text = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=120, null=True, blank=True)
    blinking_text = models.CharField(max_length=120, null=True, blank=True)
    button_text = models.CharField(max_length=120, null=True, blank=True)
    link = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    def __str__(self):
        return str(self.image)

    
    class Meta:
        ordering = ['order','-start_date', '-end_date']

    def save(self, *args, **kwargs):

        img = Image.open(self.image)

        if img.height > 200 or img.width > 200:

            output_size = (580, 1920)
            img.thumbnail(output_size)
            img = img.convert('RGB')
            output = BytesIO()
            img.save(output, format='JPEG')
            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            self.image = InMemoryUploadedFile(output, 'ImageField',
                                            f'{self.image.name.split(".")[0]}.jpg',
                                            'image/jpeg', sys.getsizeof(output),
                                            None)
        super(Slider, self).save(*args, **kwargs)