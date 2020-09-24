from django.urls import path
from . import views
app_name = 'Delivery'


urlpatterns = [

    path('shipping_view/', views.shipping_view, name='shipping_view'),

]