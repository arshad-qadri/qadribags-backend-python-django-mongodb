from common.authentication import AuthenticatedAPIView
from rest_framework import status

from customers.models import Customer
from products.models import Product

from common.response import (
    success_response,
    error_response,
)

from common.constants import Messages

from common.utils import (
    generate_order_number,
)

from .models import (
    Order,
    OrderItem,
)
from .serializers import OrderSerializer


def _calculate_payment_details(payment_type, amount_paying, grand_total):
    payment_type = str(payment_type or "credit").strip().lower()

    try:
        amount_paying = float(amount_paying or 0)
    except (TypeError, ValueError):
        return None, error_response(
            Messages.AMOUNT_PAYING_INVALID,
            None,
            status.HTTP_400_BAD_REQUEST,
        )

    if amount_paying < 0:
        return None, error_response(
            Messages.AMOUNT_PAYING_NEGATIVE,
            None,
            status.HTTP_400_BAD_REQUEST,
        )

    if payment_type == "credit":
        return (
            {
                "payment_type": "CREDIT",
                "paid_amount": 0,
                "due_amount": grand_total,
                "payment_status": "CREDIT",
            },
            None,
        )

    if amount_paying > grand_total:
        return None, error_response(
            Messages.AMOUNT_PAYING_EXCEEDS_TOTAL,
            None,
            status.HTTP_400_BAD_REQUEST,
        )

    due_amount = grand_total - amount_paying

    if due_amount == 0:
        payment_status = "PAID"
    elif amount_paying > 0:
        payment_status = "PARTIAL_PAID"
    else:
        payment_status = "CREDIT"

    return (
        {
            "payment_type": payment_type.upper(),
            "paid_amount": amount_paying,
            "due_amount": due_amount,
            "payment_status": payment_status,
        },
        None,
    )


def _build_order_items(order_items):
    final_order_items = []
    grand_total = 0
    stock_updates = []

    for item in order_items:
        sku = item.get("sku")
        quantity = item.get("quantity")

        if not sku or not quantity:
            return None, None, error_response(
                Messages.SKU_AND_QUANTITY_REQUIRED,
                None,
                status.HTTP_400_BAD_REQUEST,
            )

        if quantity <= 0:
            return None, None, error_response(
                Messages.QUANTITY_MUST_BE_POSITIVE,
                None,
                status.HTTP_400_BAD_REQUEST,
            )

        product = Product.objects(sku=sku).first()
        if not product:
            return None, None, error_response(
                Messages.product_not_found_for_sku(sku),
                None,
                status.HTTP_404_NOT_FOUND,
            )

        if quantity > product.stock:
            return None, None, error_response(
                Messages.INSUFFICIENT_STOCK,
                {
                    "sku": sku,
                    "name": product.name,
                    "available_stock": product.stock,
                },
                status.HTTP_400_BAD_REQUEST,
            )

        grand_total += quantity * product.price
        final_order_items.append(OrderItem(sku=product.sku, quantity=quantity))
        stock_updates.append((product, quantity))

    return final_order_items, grand_total, stock_updates, None


def _apply_stock_updates(stock_updates):
    for product, quantity in stock_updates:
        product.stock -= quantity
        product.save()


def _restore_existing_order_stock(order):
    restored_products = []

    for item in order.items:
        product = Product.objects(sku=item.sku).first()
        if product:
            product.stock += item.quantity
            product.save()
            restored_products.append((product, item.quantity))

    return restored_products


def _rollback_restored_stock(restored_products):
    for product, quantity in restored_products:
        product.stock -= quantity
        product.save()


class CreateOrderView(AuthenticatedAPIView):
    def post(self, request):
        try:
            customer_id = request.data.get("customer_id")
            order_items = request.data.get("order_items", [])
            payment_type = (
                str(request.data.get("payment_type", "credit")).strip().lower()
            )
            payment_mode = str(request.data.get("payment_mode", "")).strip()
            amount_paying = request.data.get("amount_paying", 0)

            if not customer_id:
                return error_response(
                    Messages.ALL_FIELDS_REQUIRED,
                    {"missing_fields": ["customer_id"]},
                    status.HTTP_400_BAD_REQUEST,
                )

            if not order_items:
                return error_response(
                    Messages.ORDER_ITEMS_REQUIRED,
                    None,
                    status.HTTP_400_BAD_REQUEST,
                )

            customer = Customer.objects(customer_id=customer_id).first()

            if not customer:
                return error_response(
                    Messages.CUSTOMER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            final_order_items, grand_total, stock_updates, order_error = _build_order_items(order_items)
            if order_error:
                return order_error

            payment_details, payment_error = _calculate_payment_details(
                payment_type,
                amount_paying,
                grand_total,
            )
            if payment_error:
                return payment_error

            _apply_stock_updates(stock_updates)

            order = Order(
                order_number=generate_order_number(),
                customer_id=customer_id,
                items=final_order_items,
                grand_total=grand_total,
                payment_type=payment_details["payment_type"],
                payment_mode=payment_mode,
                paid_amount=payment_details["paid_amount"],
                due_amount=payment_details["due_amount"],
                payment_status=payment_details["payment_status"],
            )

            order.save()

            return success_response(
                {
                    "order_number": order.order_number,
                    "grand_total": grand_total,
                    "payment_type": order.payment_type,
                    "payment_mode": order.payment_mode,
                    "paid_amount": order.paid_amount,
                    "due_amount": order.due_amount,
                    "payment_status": order.payment_status,
                },
                Messages.ORDER_CREATED,
                status.HTTP_201_CREATED,
            )

        except Exception as e:
            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EditOrderView(AuthenticatedAPIView):
    def put(self, request, order_number):
        try:
            order = Order.objects(order_number=order_number).first()

            if not order:
                return error_response(
                    Messages.ORDER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            customer_id = request.data.get("customer_id", order.customer_id)
            order_items = request.data.get("order_items")
            payment_type = request.data.get("payment_type", order.payment_type)
            payment_mode = str(request.data.get("payment_mode", order.payment_mode)).strip()
            amount_paying = request.data.get("amount_paying", order.paid_amount)

            customer = Customer.objects(customer_id=customer_id).first()
            if not customer:
                return error_response(
                    Messages.CUSTOMER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            existing_items = [{"sku": item.sku, "quantity": item.quantity} for item in order.items]
            updated_items = order_items if order_items is not None else existing_items

            if not updated_items:
                return error_response(
                    Messages.ORDER_ITEM_REQUIRED,
                    None,
                    status.HTTP_400_BAD_REQUEST,
                )

            existing_skus = {item["sku"] for item in existing_items}
            updated_skus = {item.get("sku") for item in updated_items}
            new_skus = updated_skus - existing_skus

            if new_skus:
                return error_response(
                    Messages.NEW_ITEMS_NOT_ALLOWED_ON_ORDER_EDIT,
                    {"invalid_skus": list(new_skus)},
                    status.HTTP_400_BAD_REQUEST,
                )

            restored_products = _restore_existing_order_stock(order)

            final_order_items, grand_total, stock_updates, order_error = _build_order_items(updated_items)
            if order_error:
                _rollback_restored_stock(restored_products)
                return order_error

            payment_details, payment_error = _calculate_payment_details(
                payment_type,
                amount_paying,
                grand_total,
            )
            if payment_error:
                _rollback_restored_stock(restored_products)
                return payment_error

            _apply_stock_updates(stock_updates)

            order.customer_id = customer_id
            order.items = final_order_items
            order.grand_total = grand_total
            order.payment_type = payment_details["payment_type"]
            order.payment_mode = payment_mode
            order.paid_amount = payment_details["paid_amount"]
            order.due_amount = payment_details["due_amount"]
            order.payment_status = payment_details["payment_status"]
            order.save()

            return success_response(
                {"order": OrderSerializer(order).data},
                Messages.ORDER_UPDATED,
                status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetAllOrders(AuthenticatedAPIView):
    def get(self, request):
        try:
            orders = Order.objects().order_by("-created_at")
            serializer = OrderSerializer(orders, many=True)
            return success_response(
                {"orders": serializer.data},
                Messages.ORDERS_FETCHED,
                status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetOrderById(AuthenticatedAPIView):
    def get(self, request, order_number):
        try:
            order = Order.objects(order_number=order_number).first()

            if not order:
                return error_response(
                    Messages.ORDER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            serializer = OrderSerializer(order)
            return success_response(
                {"order": serializer.data},
                Messages.ORDER_FETCHED,
                status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetOrdersbyCustomerId(AuthenticatedAPIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
            orders = Order.objects.filter(customer_id=customer_id)
            serializer = OrderSerializer(orders, many=True)
            return success_response(
                {"orders": serializer.data},
                Messages.CUSTOMER_ORDER_DATA_FETCHED,
                status.HTTP_200_OK,
            )

        except Customer.DoesNotExist:
            return error_response(
                Messages.CUSTOMER_NOT_FOUND,
                None,
                status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetOrderVlaueByCustomerId(AuthenticatedAPIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects(customer_id=customer_id).first()

            if not customer:
                return error_response(
                    Messages.CUSTOMER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            orders = Order.objects(customer_id=customer_id)
            total_order_value = sum(order.grand_total for order in orders)
            total_due_amount = sum(order.due_amount for order in orders)

            return success_response(
                {
                    "order_value": total_order_value,
                    "due_amount": total_due_amount,
                },
                Messages.CUSTOMER_ORDER_VALUE_FETCHED,
                status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                Messages.INTERNAL_SERVER_ERROR, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
            )
