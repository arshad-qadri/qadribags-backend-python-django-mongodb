from rest_framework import serializers, status
from common.authentication import AuthenticatedAPIView
from orders.models import Order
from products.models import Product
from customers.models import Customer


class OrderItemSerializer(serializers.Serializer):
    sku = serializers.CharField()
    quantity = serializers.IntegerField()

    def to_representation(self, obj):
        sku = obj.sku if hasattr(obj, "sku") else obj.get("sku")
        quantity = obj.quantity if hasattr(obj, "quantity") else obj.get("quantity")

        data = {
            "sku": sku,
            "quantity": quantity,
        }

        product = Product.objects(sku=sku).first()
        if product:
            data["id"] = str(product.id)
            data["name"] = getattr(product, "name", "")
            # data["stock"] = getattr(product, "stock", 0)
            data["price"] = getattr(product, "price", 0)

        return data


class OrderSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    order_number = serializers.CharField()
    customer_id = serializers.CharField()
    customer_details = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True)
    grand_total = serializers.FloatField()
    payment_type = serializers.CharField()
    payment_mode = serializers.CharField()
    paid_amount = serializers.FloatField()
    due_amount = serializers.FloatField()
    payment_status = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()

    def get_id(self, obj):
        return str(obj.id)

    def get_customer_details(self, obj):
        customer = Customer.objects(customer_id=obj.customer_id).first()
        if not customer:
            return None
        return {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "mobile_number": customer.mobile_number,
            "city": customer.city,
        }


class GetOrdersbyCustomerId(AuthenticatedAPIView):
    def get(self, request, customer_id):
        try:
            orders = Order.objects.filter(customer_id=customer_id)
            serializer = OrderSerializer(orders, many=True)

            return success_response(
                {"orders": serializer.data},
                "Fetched customer order data successfully",
                status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
