from django.urls import path
from . import views
from coupons.views import campaign_apply

app_name = 'coupons'
urlpatterns = [
    path('apply/', views.coupon_apply, name='apply'),
    path('campaign/', views.campaign_apply, name='campaign_apply'),# ajax-posting / name = that we will use in ajax url
    
]
