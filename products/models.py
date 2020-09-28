from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

# Create your models here.
class Category(models.Model): 
    name = models.CharField(max_length=200, db_index=True) 
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True, default= 'img/no_image.png', help_text="System may give an error if category image is not exist")
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    parent_slug = models.SlugField(max_length=200,)

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
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE) 
    name = models.CharField(max_length=200, db_index=True) 
    slug = models.SlugField(max_length=200, db_index=True) 
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, default= 'img/no_image.png')
    description = models.TextField(blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True) 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(null=True, blank=True, default=0)
    stock_managed = models.BooleanField(default=True)

    class Meta: 
        ordering = ('name',) 
        index_together = (('id', 'slug'),) 
        
    def __str__(self): return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail_view',
                       args=[self.id, self.slug])

    def get_cat_list(self):
        k = self.category # for now ignore this instance method
        
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]  