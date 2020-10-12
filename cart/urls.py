from django.urls import path
from . import views
app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('choose/<int:product_id>/', views.choose_size, name='choose_size'),
    path('remove/<int:product_id>/', views.cart_remove, 
                                     name='cart_remove'),
]
