from common.authentication import AuthenticatedAPIView
from rest_framework import status

from customers.models import Customer
from products.models import Product

from common.response import (
    success_response,
    error_response,
)

from common.constants import (
    ALL_FIELDS_REQUIRED,
    CUSTOMER_NOT_FOUND,
    PRODUCT_NOT_FOUND,
    INSUFFICIENT_STOCK,
    INTERNAL_SERVER_ERROR,
    ORDER_CREATED,
)

from common.utils import (
    generate_order_number,
)

from .models import (
    Order,
    OrderItem,
)
from .serializers import OrderSerializer

class CreateOrderView(AuthenticatedAPIView):
    def post(self, request):
        try:
            customer_id = request.data.get("customer_id")
            order_items = request.data.get("order_items", [])

            if not customer_id:
                return error_response(
                    ALL_FIELDS_REQUIRED,
                    {"missing_fields": ["customer_id"]},
                    status.HTTP_400_BAD_REQUEST,
                )

            if not order_items:
                return error_response(
                    "Order items are required",
                    None,
                    status.HTTP_400_BAD_REQUEST,
                )

            customer = Customer.objects(customer_id=customer_id).first()

            if not customer:
                return error_response(
                    CUSTOMER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            final_order_items = []

            grand_total = 0

            for item in order_items:
                sku = item.get("sku")
                quantity = item.get("quantity")

                if not sku or not quantity:

                    return error_response(
                        "Sku and quantity are required",
                        None,
                        status.HTTP_400_BAD_REQUEST,
                    )

                if quantity <= 0:
                    return error_response(
                        "Quantity must be greater than zero",
                        None,
                        status.HTTP_400_BAD_REQUEST,
                    )

                product = Product.objects(sku=sku).first()

                if not product:

                    return error_response(
                        f"Product not found for sku {sku}",
                        None,
                        status.HTTP_404_NOT_FOUND,
                    )

                if quantity > product.stock:

                    return error_response(
                        INSUFFICIENT_STOCK,
                        {
                            "sku": sku,
                            "name": product.name,
                            "available_stock": product.stock,
                        },
                        status.HTTP_400_BAD_REQUEST,
                    )

                item_total = quantity * product.price

                grand_total += item_total

                final_order_items.append(
                    OrderItem(
                        sku=product.sku,
                        quantity=quantity,
                    )
                )

                product.stock -= quantity

                product.save()

            order = Order(
                order_number=generate_order_number(),
                customer_id=customer_id,
                items=final_order_items,
                grand_total=grand_total,
                paid_amount=0,
                due_amount=grand_total,
                payment_status="UNPAID",
            )

            order.save()

            return success_response(
                {
                    "order_number": order.order_number,
                    "grand_total": grand_total,
                    "due_amount": grand_total,
                },
                ORDER_CREATED,
                status.HTTP_201_CREATED,
            )

        except Exception as e:
            return error_response(
                INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ger order details by id
# db.orders.aggregate([
#   {$match:{
#     "order_number":"QB-ORD-E831E52026-0002"
#   }},
#   {
#     $lookup: {
#       from: "customers",
#       localField: "customer_id",
#       foreignField: "customer_id",
#       as: "customerDetails"
#     }
#   },
#   {
#     $lookup: {
#       from: "products",
#       localField: "items.sku",
#       foreignField: "sku",
#       as: "productDetails"
#     }
#   },
#   {
#     $project:{
#       items:0,
#       customer_id:0
#     }
#   }
# ])


# db.customers.aggregate([
#   {$match:{
#     "customer_id":"QB-CUST-E60786-001"
#   }},
#   {
#     $lookup: {
#       from: "orders",
#       localField: "customer_id",
#       foreignField: "customer_id",
#       as: "orderDetails"
#     }
#   },
#   {
#     $lookup: {
#       from: "products",
#       localField: "orderDetails.items.sku",
#       foreignField: "sku",
#       as: "orderDetails.productDetails"
#     }
#   },
#   {
#     $project:{
#       customer_id:0
#     }
#   }
# ])


class GetOrdersbyCustomerId(AuthenticatedAPIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
            orders = Order.objects.filter(customer_id=customer_id)
            serializer = OrderSerializer(orders, many=True)
            return success_response(
                {"orders":serializer.data}, "Fetched customer order data successfully", status.HTTP_200_OK
            )
            
        except Customer.DoesNotExist:
            return error_response(
                CUSTOMER_NOT_FOUND,
                None,
                status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return error_response(
                INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
