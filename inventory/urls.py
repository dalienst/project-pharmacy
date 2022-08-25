from inventory.views import (
    InventoryDetailView,
    InventoryListCreateView,
    InventoryListView,
    CartItemListCreateView,
    CartItemDetailView,
    OrderDetailView,
    OrderListCreateView,
)
from django.urls import path

urlpatterns = [
    path("product/", InventoryListCreateView.as_view(), name="product-list"),
    path("product/<str:id>/", InventoryDetailView.as_view(), name="product-detail"),
    path("products/", InventoryListView.as_view(), name="all-products"),

    path("cart/", CartItemListCreateView.as_view(), name="cart"),
    path("cart/<str:id>/", CartItemDetailView.as_view(), name="cart-detail"),

    path("order/", OrderListCreateView.as_view(), name="order-list"),
    path("order/<str:id>/", OrderDetailView.as_view(), name="order-detail"),
]