from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import ProductImage, Variation, Product, Category
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html




class ProductResource(resources.ModelResource):
    category = Field(
            column_name='category',
            attribute='category',
            widget=ForeignKeyWidget(Category, 'name')
            )
    class Meta:
        model = Product
        skip_unchanged = True
        report_skipped = False
        #published = Field(attribute='created', column_name='created_date')
        fields = ('category__parent','created')
        #exclude = ('imported', )
        #export_order = ('id', 'name', 'category__name','created')
        #import_id_fields = ('isbn',)   
        #widgets = {'published': {'format': '%d.%m.%Y'},}
    # def dehydrate_full_title(self, product):
    #     return '%s by %s' % (product.name, product.category.name)
class VariationResource(resources.ModelResource):
    product = Field(
            column_name='product',
            attribute='product',
            widget=ForeignKeyWidget(Product, 'name')
            )

    class Meta:
        model = Variation
        #import_id_fields = ('id',) 
        #fields = ('product__category','product__available')
        #fields = ('id','product','product__id','product__color', 'product__slug','category','title','sku','price','cost','sale_price',)
      
        #export_order = ('id', 'product__name','product__slug','product__color','product__category__name', 'category','title','sku','price','cost','sale_price',)
        
        #exclude = ('id', )
            
        
    

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
class ProductAdmin(ImportExportModelAdmin): 
    list_display = ['image_tag','name', 'category', 'available', 'created', 'updated'] 
    list_filter = ['category', 'created','available', 'updated'] 
    search_fields = ('name', 'description', )
    list_editable = [ 'available'] 
    prepopulated_fields = {'slug': ('name',)}
    save_as = True
    inlines = [ImageInline, VariationInline]
    resource_class = ProductResource

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: auto; height:45px;" />'.format(obj.image.url))

@admin.register(Variation) 
class VariationAdmin(ImportExportModelAdmin):
    list_display = ['image_tag','product','category','title','sku', 'price', 'cost', 'sale_price','ecomdashid','updated','active']
    list_editable = ['category','title','sku', 'price', 'cost', 'sale_price','active']
    resource_class = VariationResource

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: auto; height:45px;" />'.format(obj.product.image.url))


#admin.site.register(Variation)
#admin.site.register(AttributeBase)
#admin.site.register(Attribute)
#admin.site.register(ProductAttribute)