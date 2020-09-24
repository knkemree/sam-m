from django.urls import path
from orders import views
app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('admin/order/<int:order_id>/', views.admin_order_detail,name='admin_order_detail'),
    #path('shipping_apply/', views.shipping_apply, name='shipping_apply'),
    #path('admin/order/<int:order_id>/pdf/',views.admin_order_pdf,name='admin_order_pdf'),
    
]
