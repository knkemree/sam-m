from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render, redirect

from .models import Customers

# Register your models here.

class CustomersAdmin(UserAdmin):
    
    list_display = ('email', 'company_name', 'first_name', 'last_name','ein', 'ein_verified','is_active','phone','last_login', 'date_joined' )
    search_fields = ('email', 'company_name', 'first_name', 'last_name','ein','phone')
    ordering = ['-date_joined']
    
    # def get_readonly_fields(self, request, obj=None):
    #     try:
    #         if obj.ein_verified == True:  # editing an existing object
                
    #             self.readonly_fields = ('ein',)
    #         else:
    #             self.readonly_fields = ()
    #         return self.readonly_fields
    #     except:
    #         pass

        

    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ()
    fieldsets = ()
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ("email", "company_name",)}),
    )
    


    
admin.site.register(Customers, CustomersAdmin)