from django.urls import path
from ship_station.views import IndexView, InventoryLogListView, ProductDetailView, ProductListView, decrease, increase, lookup, update_source_file


app_name = 'ship_station'


urlpatterns = [
    path('update_source_file/',update_source_file,name='update_source_file'),
    path('lookup/',lookup,name='lookup'),
    path('index/',IndexView.as_view(),name='index'),
    path('increase/',increase,name='increase'),
    path('decrease/',decrease,name='decrease'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('inventorylogs/', InventoryLogListView.as_view(), name='inventorylog-list'),
]