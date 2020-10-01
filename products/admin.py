from django.contrib import admin

from .models import Product, Category
from django.utils.safestring import mark_safe
from products.models import ProductImage



# Register your models here.
class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# class VariationInline(admin.TabularInline):
#     model = Variation
#     extra = 1

@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin): 
    # list_display = ['parent','name', 'slug', 'image'] 
    prepopulated_fields = {'slug': ('name',)} 

    
    
@admin.register(Product) 
class ProductAdmin(admin.ModelAdmin): 
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated'] 
    list_filter = ['category','available', 'created', 'updated'] 
    list_editable = ['price', 'available',] 
    prepopulated_fields = {'slug': ('name',)}
    save_as = True
    inlines = [ImageInline, 
    ]

# admin.site.register(AttributeBase)
# admin.site.register(Attribute)
# admin.site.register(ProductAttribute)