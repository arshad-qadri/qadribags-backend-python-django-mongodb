from django.urls import path
from .views import (
    GetTotalStock,
    GetTotalLowStock,
    GetTotalValue,
    InventoryByCategoryPercentage,
    GetLowStockAlerts,GetTotalProductCount
)

urlpatterns = [
    path("stock", GetTotalStock.as_view()),
    path("low-stock", GetTotalLowStock.as_view()),
    path("catalog-value", GetTotalValue.as_view()),
    path("inventory-by-ctagory-percentage", InventoryByCategoryPercentage.as_view()),
    path("low-stock-alerts", GetLowStockAlerts.as_view()),
    path("product-count", GetTotalProductCount.as_view()),
]
