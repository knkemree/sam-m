from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render, redirect

from .models import Customers

# Register your models here.

class CustomersAdmin(UserAdmin):
    
    list_display = ('email', 'company_name', 'first_name', 'last_name','ein', 'ein_verified','is_active','phone','last_login', 'date_joined' )
    search_fields = ('email', 'company_name', 'first_name', 'last_name','ein','phone')
    ordering = ['-date_joined']
    readonly_fields = ('ein','stripe_customer','date_joined','last_login')
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','phone','admin','staff','is_superuser',)}),
        ('Permissions', {'fields': ('user_permissions','groups',
        )}),
        (('Important dates'), {'fields': ('date_joined','last_login',)}),
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)}
        ),
    )
    


    
admin.site.register(Customers, CustomersAdmin)