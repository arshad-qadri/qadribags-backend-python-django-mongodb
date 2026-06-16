from django.urls import path
from .views import (
    CreateOrderView,
    EditOrderView,
    GetOrdersbyCustomerId,
    GetOrderVlaueByCustomerId,
    GetAllOrders,
    GetOrderById,
)

urlpatterns = [
    path("create", CreateOrderView.as_view()),
    path("edit/<str:order_number>", EditOrderView.as_view()),
    path("customer-order-list/<str:customer_id>", GetOrdersbyCustomerId.as_view()),
    path("order-value/<str:customer_id>", GetOrderVlaueByCustomerId.as_view()),
    path("all-orders", GetAllOrders.as_view()),
    path("order/<str:order_number>", GetOrderById.as_view()),
]
