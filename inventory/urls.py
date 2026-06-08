from django.urls import path
from .views import (
    GetTotalAvailableStockAndProductCount,
    GetLowStockProductCount,
    GetTotalValue,
    InventoryByCategoryPercentage,
    GetLowStockAlerts,
    GetTotalProductCount,
)

urlpatterns = [
    path("total-available-stock-product-count", GetTotalAvailableStockAndProductCount.as_view()),
    path("low-stock-product-count", GetLowStockProductCount.as_view()),
    path("catalog-value", GetTotalValue.as_view()),
    path("inventory-by-ctagory-percentage", InventoryByCategoryPercentage.as_view()),
    path("low-stock-alerts", GetLowStockAlerts.as_view()),
    path("product-count", GetTotalProductCount.as_view()),
]
