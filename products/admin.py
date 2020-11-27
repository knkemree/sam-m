import admin_thumbnails
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import ProductImage, Variation, Product, Category
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html





class ProductResource(resources.ModelResource):
    category_name = Field(
            column_name='category_name',
            attribute='category',
            widget=ForeignKeyWidget(Category, 'name')
            )
    
    class Meta:
        model = Product
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('name',)
        #published = Field(attribute='created', column_name='created_date')
        fields = ('category_name','name','color','slug','description','available')
        #exclude = ('imported', )
        #export_order = ('id', 'name', 'category__name','created')
           
        #widgets = {'published': {'format': '%d.%m.%Y'},}
    # def dehydrate_full_title(self, product):
    #     return '%s by %s' % (product.name, product.category.name)

    def before_import_row(self, row, **kwargs):
        
        
        #Category.objects.get_or_create(name=row.get('child_collection'))
        #row['child_collection'] = cat.name
        #cat = Category.objects.get_or_create(id=row.get('category'))
        #category = Category.objects.get(id=row['category'])
        #Product.objects.get_or_create(id=row.get('id'), category_id=row['category'])
        
        
        
        
        #Variation.objects.get_or_create(product=row.get('product.id'), sku=row.get('sku')) 

        return super().before_import_row(row, **kwargs)

class VariationResource(resources.ModelResource):

    product_name = Field(
            column_name='product_name',
            attribute='product',
            widget=ForeignKeyWidget(Product, 'name')
            )

    child_collection = Field(
            column_name='child_collection',
            attribute='product__category',
            widget=ForeignKeyWidget(Category, 'name')
            )


    # parent_collection = Field(
    #         column_name='parent_collection',
    #         attribute='product__category',
    #         widget=ForeignKeyWidget(Category, 'parent')
    #         )

    

    skip_unchanged = True
    report_skipped = True

    class Meta:
        model = Variation
        import_id_field = 'sku'
        import_id_fields = ('sku','product_name',) 
        fields = ('product_name','sku','title','child_collection','price','cost','sale_price','product__image','active')
        
        #fields = ('product','product__color','child_collection','product__image','product__available','id','sku','title','price','cost','sale_price','active')
        #export_order = ('product','product__color','child_collection','product__image','product__available','id','sku','title','price','cost','sale_price','active')
        #exclude = ('ecomdashid', )
            
    def before_import_row(self, row, **kwargs):
        
        
        
        #row['child_collection'] = cat.name
        Product.objects.get_or_create(name=row.get('product_name'))
        
        
        
        
        #Variation.objects.get_or_create(product=row.get('product.id'), sku=row.get('sku')) 

        return super().before_import_row(row, **kwargs)
        

    # def before_save_instance(self, row, **kwargs):
    #     pass

# Register your models here.
@admin_thumbnails.thumbnail('image')
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
    list_display = ['image_tag','name','parent', 'slug', 'active'] 
    list_display_links = ['image_tag','name',]
    list_filter = ['parent']
    list_editable = ['active','parent']
    prepopulated_fields = {'slug': ('name',)} 

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: auto; height:50px;" />'.format(obj.image.url))

    
    
@admin.register(Product) 
@admin_thumbnails.thumbnail('image')
class ProductAdmin(ImportExportModelAdmin): 
    #list_display = ['name'] 
    list_display = ['image_tag','name', 'category', 'available', 'created', 'updated'] 
    #list_display_links = ['image_tag','name',]
    #list_filter = ['category', 'created','available', 'updated','created'] 
    search_fields = ('name', 'description', 'slug','id',)
    #list_editable = [ 'available','category'] 
    list_editable = [ 'available'] 
    list_per_page = 100
    #list_select_related = ['category']
    prepopulated_fields = {'slug': ('name',)}
    save_as = True
    inlines = [ImageInline, VariationInline]
    resource_class = ProductResource

    
    def queryset(self, request):
        return super(ProductAdmin, self).queryset(request).select_related("category")


    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: auto; height:45px;" />'.format(obj.image.url))
    

@admin.register(Variation) 
class VariationAdmin(ImportExportModelAdmin):
    list_display = ['image_tag','product','category','title','sku', 'price', 'cost', 'sale_price','ecomdashid','updated','active','clearance']
    list_display_links = ['image_tag','product',]
    list_filter = ['product__category','category','active', 'updated',]
    list_editable = ['category','title','sku', 'price', 'cost', 'sale_price','active']
    search_fields = ('sku','id','title','category')
    list_per_page = 50
    save_as = True
    resource_class = VariationResource

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: auto; height:45px;" />'.format(obj.product.image.url))

    def clearance(self,obj):
        if obj.sale_price:
            return True
        else:
            return False

@admin.register(ProductImage)
@admin_thumbnails.thumbnail('image')
class ProductImageAdmin(ImportExportModelAdmin):
    list_display = ['image_tag','product','order','create_at','update_at']
    list_display_links = ['image_tag','product',]
    list_filter = ["product"]
    search_fields = ('product','image',)
    list_editable = ['order']

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: auto; height:45px;" />'.format(obj.image.url))


#admin.site.register(AttributeBase)
#admin.site.register(Attribute)
#admin.site.register(ProductAttribute)