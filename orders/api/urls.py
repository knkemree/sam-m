from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.api.views import OrderList
app_name = 'orders'

router_orders = DefaultRouter()
router_orders.register(r"orders", OrderList)

urlpatterns = [
    path("", include((router_orders.urls, 'orders'), namespace='orders')),
    # path('', ProductList.as_view(), name='ProductList'),
]