from django.contrib import admin
from .models import Product, Category
from django.utils.safestring import mark_safe
from products.models import ProductImage, Variation



# Register your models here.
class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

# class ProductAttributeInline(admin.TabularInline):
#     model = ProductAttribute
#     extra = 1

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0

@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin): 
    # list_display = ['parent','name', 'slug', 'image'] 
    prepopulated_fields = {'slug': ('name',)} 

    
    
@admin.register(Product) 
class ProductAdmin(admin.ModelAdmin): 
    list_display = ['name', 'category', 'available', 'created', 'updated'] 
    list_filter = ['category', 'created','available', 'updated'] 
    list_editable = [ 'available'] 
    prepopulated_fields = {'slug': ('name',)}
    save_as = True
    inlines = [ImageInline, VariationInline]


#admin.site.register(AttributeBase)
#admin.site.register(Attribute)
#admin.site.register(ProductAttribute)