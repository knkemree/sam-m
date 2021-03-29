from orders.models import Order
from orders.api.serializers import OrderSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework import mixins
from rest_framework import viewsets

class OrderList(mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]