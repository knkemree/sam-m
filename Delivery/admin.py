from django.contrib import admin
from .models import Delivery_methods

# Register your models here.

@admin.register(Delivery_methods)
class Delivery_methodsAdmin(admin.ModelAdmin):
    
    list_display = ["delivery_method", "fee"]