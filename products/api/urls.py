from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.api.views import CategoryList, ProductList
app_name = 'products'

router_products = DefaultRouter()
router_products.register(r"products", ProductList)
router_products.register(r"categories", CategoryList)

urlpatterns = [
    path("", include((router_products.urls, 'products'), namespace='products')),
    # path('', ProductList.as_view(), name='ProductList'),
]