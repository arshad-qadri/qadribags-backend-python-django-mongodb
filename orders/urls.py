from django.urls import path
from .views import CreateOrderView,GetOrdersbyCustomerId

urlpatterns = [
    path("create", CreateOrderView.as_view()),
    path("customer-order-list/<str:customer_id>", GetOrdersbyCustomerId.as_view()),
]
