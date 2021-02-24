from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import Order, OrderItem
import csv
import datetime
from django.db.models import Count






def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = 'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not \
    field.many_to_many and not field.one_to_many] 
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    #readonly_fields = ('cost',)
    can_delete = False
    extra = 0
    raw_id_fields = ['product']
    
def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    list_display = ['id','company_name', 'email',
                    'address', 'postal_code', 'city', 'payment','fulfillment','delivery_method',"order_total","order_profit","profit_margin",
                    'created', 'updated',order_detail,] #order_pdf
    list_filter = ['payment', 'created', 'updated', 'fulfillment','company_name']
    readonly_fields = ('order_total','order_profit','profit_margin','braintree_id',"campaign_discount",'campaign','delivery_method')
    inlines = [OrderItemInline]
    actions = [export_to_csv]