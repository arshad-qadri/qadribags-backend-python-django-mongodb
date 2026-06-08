from rest_framework import status
import random
from common.authentication import AuthenticatedAPIView
from common.constants import (
    # PRODUCT_CREATED,
    # PRODUCT_ALREADY_EXIST,
    # ALL_FIELDS_REQUIRED,
    INTERNAL_SERVER_ERROR,
)

from common.response import (
    success_response,
    error_response,
)
from products.models import Product
from products.serializers import ProductSerializer


class GetTotalAvailableStockAndProductCount(AuthenticatedAPIView):
    def get(self, request):
        try:
            total_available_stock = Product.objects.sum("stock")
            total_product_count = Product.objects.count()
            return success_response(
                {"total_available_stock": total_available_stock, "total_product_count":total_product_count}, "Stock fetched successfully"
            )
        except Exception as e:
            return error_response(
                INTERNAL_SERVER_ERROR, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetLowStockProductCount(AuthenticatedAPIView):
    def get(self, request):
        try:
            total_low_stock = Product.objects.filter(stock__lte=10).count()
            return success_response(
                {"lowStock": total_low_stock},
                "Low stock product count fetched successfully",
                status.HTTP_200_OK,
            )
        except Exception as e:

            return error_response(
                INTERNAL_SERVER_ERROR, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetTotalValue(AuthenticatedAPIView):
    def get(self, request):
        try:
            pipeline = [
                {"$project": {"product_value": {"$multiply": ["$price", "$stock"]}}},
                {"$group": {"_id": None, "total_value": {"$sum": "$product_value"}}},
            ]

            result = list(Product.objects.aggregate(*pipeline))

            if result:
                total_catalog_value = result[0]["total_value"]
            else:
                total_catalog_value = 0
            return success_response(
                {"value": total_catalog_value},
                "Catalog value fetched successfully",
                status.HTTP_200_OK,
            )
        except Exception as e:

            return error_response(
                INTERNAL_SERVER_ERROR, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InventoryByCategoryPercentage(AuthenticatedAPIView):
    def get(self, request):
        try:
            pipeline = [
                {
                    "$facet": {
                        "grand_total": [
                            {"$group": {"_id": None, "total": {"$sum": "$stock"}}}
                        ],
                        "category_totals": [
                            {
                                "$group": {
                                    "_id": "$category",
                                    "count": {"$sum": "$stock"},
                                }
                            }
                        ],
                    }
                },
                {"$unwind": "$grand_total"},
                {"$unwind": "$category_totals"},
                {
                    "$project": {
                        "_id": 0,
                        "category": "$category_totals._id",
                        "total_stock": "$category_totals.count",
                        "percentage": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {
                                            "$divide": [
                                                "$category_totals.count",
                                                "$grand_total.total",
                                            ]
                                        },
                                        100,
                                    ]
                                },
                                2,
                            ]
                        },
                    }
                },
            ]

            result = list(Product.objects.aggregate(*pipeline))

            for item in result:
                item["color"] = f"#{random.randint(0, 0xFFFFFF):06x}"

            return success_response(
                {"categoryItems": result},
                "Catalog value fetched successfully",
                status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                INTERNAL_SERVER_ERROR, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetLowStockAlerts(AuthenticatedAPIView):
    def get(self, request):
        try:
            pipeline = [
                {"$match": {"stock": {"$lte": 10}}},
                {"$project": {"name": 1, "sku": 1, "stock": 1, "_id": 0}},
            ]
            result = list(Product.objects.aggregate(*pipeline))
            return success_response(
                {"lowStockAlerts": result},
                "Low stock alerts fetched successfully",
                status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                INTERNAL_SERVER_ERROR, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetTotalProductCount(AuthenticatedAPIView):
    def get(self, request):
        try:
            active_product_count = Product.objects.filter(status="ACTIVE").count()
            inactive_product_count = Product.objects.filter(status="INACTIVE").count()
            total_products = Product.objects.count()
            return success_response(
                {
                    "active_product_count": active_product_count,
                    "inactive_product_count": inactive_product_count,
                    "total_products":total_products
                },
                "Product count fetched successfully",
                status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                INTERNAL_SERVER_ERROR, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
            )
