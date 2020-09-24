from django.contrib import admin
from .models import Coupon, Campaign
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to',
                    'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['campaign_name', 'amount_from', 'amount_to',
                    'campaign_discount', 'active']
    list_filter = ['active']
    search_fields = ['campaign_name']