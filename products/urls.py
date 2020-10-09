from django.urls import path
from .views import  product_list_view, product_detail_view
from django.contrib.admin import views


app_name = 'products'


urlpatterns = [
    path('', product_list_view, name='product_list_view'),
    path('<slug:category_slug>/', product_list_view, name='product_list_by_category'),
    #path('category/<path:hierarchy>/',show_category, name='category'),
    path('<int:id>/<slug:slug>/', product_detail_view, name='product_detail_view'),
]
