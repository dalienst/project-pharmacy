from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from inventory.serializers import InventorySerializer, CartSerializer, OrderSerializer
from inventory.models import Inventory, CartItem, Order
from users.permissions import IsUser, UserNew

# todo: check and create permissions

class InventoryListCreateView(generics.ListCreateAPIView):
    """"""
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    # TODO: set permission to only allow employee to enter records
    permission_classes = [IsAuthenticated, IsUser]

class InventoryListView(generics.ListAPIView):
    """"""
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()

class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """"""
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    # TODO: set permission to only allow employee to enter records
    permission_classes = [IsAuthenticated, UserNew]
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Inventory deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class CartItemListCreateView(generics.ListCreateAPIView):
    """"""
    serializer_class = CartSerializer
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """"""
    serializer_class = CartSerializer
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated,]
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message":"deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

class OrderListCreateView(generics.ListCreateAPIView):
    """"""
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    # TODO: set permission to only allow employee to enter records
    permission_classes = [IsAuthenticated,]

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """"""
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    # TODO: set permission to only allow employee to enter records
    permission_classes = [IsAuthenticated,]
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Order deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )