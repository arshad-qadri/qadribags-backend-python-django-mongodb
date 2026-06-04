from django.urls import path
from .views import CreateProductView, UploadProductImageView, GetProductBySKU, GetProductList,UpdateProductView

urlpatterns = [
    path("create", CreateProductView.as_view()),
    path("update/<str:sku>", UpdateProductView.as_view()),
    path("upload-image/<str:sku>", UploadProductImageView.as_view()),
    path("list", GetProductList.as_view()),
    path("get-product-by-sku/<str:sku>", GetProductBySKU.as_view()),
]
