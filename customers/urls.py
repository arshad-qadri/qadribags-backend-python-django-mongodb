from .views import (
    CreateCustomerView,
    GetAllCustomersView,
    GetCustomerByIdView,
    UpdateCustomerView,
    DeleteCustomerView,
    MakeCustomerActiveInactiveView,
)
from django.urls import path

urlpatterns = [
    path("create", CreateCustomerView.as_view()),
    path("list", GetAllCustomersView.as_view()),
    path("customer/get-by-id/<str:customer_id>", GetCustomerByIdView.as_view()),
    path("customer/update-by-id/<str:customer_id>", UpdateCustomerView.as_view()),
    path(
        "customer/active-inactive-by-id/<str:customer_id>",
        MakeCustomerActiveInactiveView.as_view(),
    ),
]
