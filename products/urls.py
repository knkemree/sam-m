from django.urls import path
from .views import  product_list_view, product_detail_view, choose_size
from django.contrib.admin import views
from products.views import clearance, post_search, updateQtyView


app_name = 'products'


urlpatterns = [
    path('', product_list_view, name='product_list_view'),
    path('search/', post_search, name='post_search'),
    path('<slug:category_slug>/', product_list_view, name='product_list_by_category'),
    path('choose/<int:product_id>/', choose_size, name='choose_size'),
    path('<int:id>/<slug:slug>/', product_detail_view, name='product_detail_view'),
    path('<int:id>/<slug:slug>/<int:variantid>/', product_detail_view, name='product_detail_view_by_variant'),
    path('ecomdash/updateQty/', updateQtyView, name='updateQty'),
    path('all_products/clearance/', clearance, name='clearance'),
    
    
]
