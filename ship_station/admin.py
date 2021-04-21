from django.contrib import admin
from .models import File
from ship_station.models import ArchivedBrand, ArchivedColor, ArchivedInventoryLog, ArchivedModel, ArchivedProduct, ArchivedSize, Brand, Color, InventoryLog, Model, Product, Size

class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ['product','quantity','in_stock']
    
    readonly_fields = ['in_stock']

    def in_stock(self, obj):
        return obj.current_stock

class ProductAdmin(admin.ModelAdmin):
    list_display = ['model','size','color','in_stock','created_at']
    fields = ['ean','in_stock','name','model','size','color','note']
    #readonly_fields = ['ean','in_stock','name','model','size','color',]
    readonly_fields = ['in_stock']
    list_filter = ['size','color','model','model__brand']
    search_fields = ['size__name','color__name','model__name','model__brand__name']

    def in_stock(self, obj):
        return obj.current_stock

class ArchivedProductAdmin(admin.ModelAdmin):
    list_display = ['model','size','color','created_at']
    fields = ['ean','name','model','size','color','note','deleted_ts']
    readonly_fields = ['deleted_ts']

# Register your models here.
admin.site.register(File)
admin.site.register(Product, ProductAdmin)
admin.site.register(ArchivedProduct, ArchivedProductAdmin)
admin.site.register(Model)
admin.site.register(ArchivedModel)
admin.site.register(Size)
admin.site.register(ArchivedSize)
admin.site.register(Color)
admin.site.register(ArchivedColor)
admin.site.register(Brand)
admin.site.register(ArchivedBrand)
admin.site.register(InventoryLog, InventoryLogAdmin)
admin.site.register(ArchivedInventoryLog)
