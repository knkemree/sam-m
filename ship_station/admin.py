from django.contrib import admin
from .models import File
from ship_station.models import ArchivedBrand, ArchivedColor, ArchivedInventoryLog, ArchivedModel, ArchivedProduct, ArchivedSize, Brand, Color, InventoryLog, Model, Product, Size
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin

class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ['product','quantity','in_stock']
    
    readonly_fields = ['in_stock']

    def in_stock(self, obj):
        return obj.current_stock

class ProductResource(resources.ModelResource):
    size_name = Field(
            column_name='size_name',
            attribute='size',
            widget=ForeignKeyWidget(Size, 'name')
            )

    color_name = Field(
            column_name='color_name',
            attribute='color',
            widget=ForeignKeyWidget(Color, 'name')
            )

    model_styleID = Field(
            column_name='model_styleID',
            attribute='model',
            widget=ForeignKeyWidget(Model, 'styleID')
            )
    
    class Meta:
        model = Product
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('gtin',)
        #published = Field(attribute='created', column_name='created_date')
        fields = ('sku','gtin','model_name','size_name','model_styleID','color_name',)
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

class ProductAdmin(ImportExportModelAdmin):
    list_display = ['id','model','size','color','in_stock','created_at']
    fields = ['sku','skuID_Master','gtin','ean2','in_stock','name','model','size','color','note']
    #readonly_fields = ['ean','in_stock','name','model','size','color',]
    readonly_fields = ['in_stock']
    list_filter = ['size','color','model','model__brand']
    search_fields = ['size__name','color__name','model__name','model__brand__name','gtin']
    resource_class = ProductResource

    def in_stock(self, obj):
        return obj.current_stock

class ArchivedProductAdmin(admin.ModelAdmin):
    list_display = ['model','size','color','created_at']
    fields = ['ean','name','model','size','color','note','deleted_ts']
    readonly_fields = ['deleted_ts']

class SizeResource(resources.ModelResource):
    class Meta:
        model = Size
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('name',)
        fields = ('name','sizeCode')

class SizeAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display= ['name', 'sizeCode']
    resource_class = SizeResource

class ColorResource(resources.ModelResource):
    class Meta:
        model = Color
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('name',)
        fields = ('name','colorCode')

class ColorAdmin(ImportExportModelAdmin):
    list_display= ['name','colorCode']
    search_fields = ['name']
    resource_class = ColorResource

class BrandResource(resources.ModelResource):
    class Meta:
        model = Brand
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('name',)
        fields = ('name',)

class BrandAdmin(ImportExportModelAdmin):
    list_display= ['name']
    search_fields = ['name']
    resource_class = BrandResource

class ModelResource(resources.ModelResource):
    brand_name = Field(
            column_name='brand_name',
            attribute='brand',
            widget=ForeignKeyWidget(Brand, 'name')
            )
    
    class Meta:
        model = Model
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('name',)
        #published = Field(attribute='created', column_name='created_date')
        fields = ('name','styleID','brand_name',)

class ModelAdmin(ImportExportModelAdmin):
    list_display= ['brand','name','styleID']
    list_filter = ['brand']
    search_fields = ['name','brand__name']
    resource_class = ModelResource

# Register your models here.
admin.site.register(File)
admin.site.register(Product, ProductAdmin)
admin.site.register(ArchivedProduct, ArchivedProductAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(ArchivedModel)
admin.site.register(Size, SizeAdmin)
admin.site.register(ArchivedSize)
admin.site.register(Color, ColorAdmin)
admin.site.register(ArchivedColor)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ArchivedBrand)
admin.site.register(InventoryLog, InventoryLogAdmin)
admin.site.register(ArchivedInventoryLog)
