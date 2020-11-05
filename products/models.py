from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Min
from django.core.exceptions import ValidationError
from django.core.files import File
from django.utils.text import slugify


# from ckeditor.fields import RichTextField


import os
import http.client
import mimetypes
import json
import urllib.request

# Create your models here.   

class Category(models.Model): 
    name = models.CharField(max_length=200, db_index=True) 
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True, default= 'img/no_image.png', help_text="System may give an error if the category image does not exist")
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    #parent_slug = models.SlugField(max_length=200,)

    class Meta: 
        ordering = ('name',) 
        verbose_name = 'category' 
        verbose_name_plural = 'categories' 
        unique_together = [['slug', 'name']]  

    def __str__(self): 
        full_path = [self.name]                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1]) 

    def get_cat_name(self):
        return self.name

    def get_parent_name(self):
        return self.get_parent_name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category',
                       args=[self.slug])


class Product(models.Model): 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) 
    name = models.CharField(max_length=200, db_index=True) 
    color = models.CharField(max_length=200, db_index=True, blank=True, null=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True) 
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True, default= 'img/logo.png', help_text="System may give an error if product cover image does not exist")
    #image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True, default= 'img/no_image.png')
    image_url = models.URLField(blank=True, null=True)
    #description = RichTextField(blank=True, null=True) 
    #description = QuillField(blank=True, null=True)
    description = models.TextField(blank=True, null=True) 
    #price = models.DecimalField(max_digits=10, decimal_places=2)
    #sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    #cost = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True) 
    created = models.DateTimeField(auto_now_add=True, null=True) 
    updated = models.DateTimeField(auto_now=True, null=True)
    #stock = models.IntegerField(null=True, blank=True, default=0)
    #stock_managed = models.BooleanField(default=True)

    class Meta: 
        ordering = ('name',) 
        index_together = (('id', 'slug'),) 
        
    def __str__(self): 
        return self.name
    

    def get_absolute_url(self):
        return reverse('products:product_detail_view',
                       args=[self.id, self.slug])

    def get_lowest_price(self):
        return self.variation_set.all().aggregate(Min('price'))

    def get_default_image(self):
        if self.image is None:
            self.image = 'img/no_image.png'
        return self.save()
        # if self.image_url == None:
        #     result = urllib.request.urlretrieve(self.image_url)
            # self.image.save(os.path.basename(self.image_url),
            #         File(open(result[0]))
            #         )
            # return print("get remote method", result)

    def admin_image(self):
        return '<img src="%s"/>' % self.image
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    admin_image.allow_tags = True
    class Meta:
        ordering = ['-created','name']
        

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    featured = models.BooleanField(default=True)
    thumbnail = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return os.path.basename(self.image.name)
        #return self.product.name
    class Meta:
        ordering = ['order']
    
    

class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return self.all().filter(category='color')

    def packages(self):
        return self.all().filter(category='package')
    
VAR_CATEGORIES = (
    ('size', 'size'),
    ('color','color'),
    ('package', 'package')
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices= VAR_CATEGORIES, default='size')
    title = models.CharField(max_length=120) 
    sku = models.CharField(max_length=60, blank=False, unique=True, help_text="SKU must be unique") 
    #image = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, blank=True, null=True )
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0 )
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0 )
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True )
    ecomdashid = models.CharField(max_length=20, blank=True, null=True,) 
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    #clearance = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = VariationManager()

    def __str__(self): 
        return self.sku

    def get_absolute_url(self):
        return reverse('products:product_detail_view_by_variant',
                       args=[self.product.id, self.product.slug, self.id])

    # def save(self, **kwargs):

    #     return super(Variation, self).save(**kwargs)

    def clean(self):
        super().clean()
        

        conn = http.client.HTTPSConnection("ecomdash.azure-api.net")
        payload = ''
        headers = {
            'Ocp-Apim-Subscription-Key': 'ce0057d8843342c8b3bb5e8feb0664ac',
            'ecd-subscription-key': '0e26a6d3e46145d5b7dd00a9f0e23c39'
            }

        

        conn.request("GET", "/api/Inventory?Type=Product&Sku="+str(self.sku), payload, headers)
        res = conn.getresponse()
        data = res.read()
        veri = json.loads(data.decode("utf-8"))
        # for i in veri["data"]:
        #     if i["Type"]=="Kit":
        #         kit_id = int(float(i["Id"]))
        #         conn.request("GET", "/api/Inventory/"+str(kit_id)+"/kitcomponents", payload, headers)
        #         res = conn.getresponse()
        #         data = res.read()
        #         kit_veri = json.loads(data.decode("utf-8"))
        #         for i in kit_veri["data"]:
        #             parent_id = int(float(i["Product"]["Id"]))
        #             parent_sku = i["Product"]["Sku"]
        #             self.ecomdashid = parent_id
        #             self.sku = parent_sku
            
        #     elif i["Type"] = =

        
        if len(veri["data"]) == 0:
            raise ValidationError("Sku didn't match with Ecomdash records "+str(self.sku))

        try:
            if self.ecomdashid is None:
                for i in veri["data"]:
                    self.ecomdashid = i["Id"]
                    self.save()
        except:
            pass

        try:
            for i in veri["data"]:
                if self.ecomdashid != i["Id"]:
                    self.ecomdashid = i["Id"]
                    self.save()
        except:
            pass