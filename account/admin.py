from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render, redirect

from .models import Customers

# Register your models here.

class CustomersAdmin(UserAdmin):
    
    list_display = ('id', 'company_name', 'fullname','ein_verified','staff','is_active','last_login', 'date_joined' )
    search_fields = ('email', 'company_name', 'first_name', 'last_name','ein','phone')
    ordering = ['-date_joined']
    readonly_fields = ('ein','stripe_customer','date_joined','last_login','fullname')
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ('staff',)
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
    
    def fullname(self,obj):
        return obj.get_full_name()


    
admin.site.register(Customers, CustomersAdmin)