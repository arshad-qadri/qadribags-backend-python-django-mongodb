from common.authentication import AuthenticatedAPIView
from rest_framework import status
from .serializers import CustomerSerializer
from bson.errors import InvalidId
from common.utils import generate_customer_id

from common.response import (
    success_response,
    error_response,
)

from common.constants import Messages

from .models import Customer


class CreateCustomerView(AuthenticatedAPIView):

    def post(self, request):

        try:

            name = request.data.get("name")
            mobile_number = request.data.get("mobile_number")
            customer_id = generate_customer_id()
            required_fields = [
                "name",
                "mobile_number",
            ]

            missing_fields = [
                field for field in required_fields if not request.data.get(field)
            ]

            if missing_fields:
                return error_response(
                    Messages.ALL_FIELDS_REQUIRED,
                    {"missing_fields": missing_fields},
                    status.HTTP_400_BAD_REQUEST,
                )

            existing_customer = Customer.objects(mobile_number=mobile_number).first()

            if existing_customer:

                return error_response(
                    Messages.CUSTOMER_ALREADY_EXIST,
                    None,
                    status.HTTP_400_BAD_REQUEST,
                )

            customer = Customer(
                name=name,
                mobile_number=mobile_number,
                customer_id=customer_id,
                email=request.data.get("email"),
                address=request.data.get("address"),
                city=request.data.get("city"),
                state=request.data.get("state"),
                pincode=request.data.get("pincode"),
                gst_number=request.data.get("gst_number"),
                customer_type=request.data.get(
                    "customer_type",
                    "RETAIL",
                ),
            )

            customer.save()

            return success_response(
                {"id": str(customer.id)},
                Messages.CUSTOMER_CREATED,
                status.HTTP_201_CREATED,
            )

        except Exception as e:

            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetAllCustomersView(AuthenticatedAPIView):

    def get(self, request):

        try:

            customers = Customer.objects()

            return success_response(
                CustomerSerializer.serialize_many(customers),
                Messages.CUSTOMERS_FETCHED,
                status.HTTP_200_OK,
            )

        except Exception as e:

            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetCustomerByIdView(AuthenticatedAPIView):

    def get(self, request, customer_id):

        try:

            customer = Customer.objects(customer_id=customer_id).first()

            if not customer:

                return error_response(
                    Messages.CUSTOMER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            return success_response(
                CustomerSerializer.serialize(customer),
                Messages.CUSTOMER_FETCHED,
                status.HTTP_200_OK,
            )

        except InvalidId:

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


class UpdateCustomerView(AuthenticatedAPIView):

    def put(self, request, customer_id):

        try:

            customer = Customer.objects(customer_id=customer_id).first()

            if not customer:

                return error_response(
                    Messages.CUSTOMER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            mobile_number = request.data.get("mobile_number")

            if mobile_number:

                existing_customer = Customer.objects(
                    mobile_number=mobile_number
                ).first()

                if existing_customer and str(existing_customer.id) != str(customer.id):

                    return error_response(
                        Messages.CUSTOMER_ALREADY_EXIST,
                        None,
                        status.HTTP_400_BAD_REQUEST,
                    )

            customer.name = request.data.get(
                "name",
                customer.name,
            )

            customer.mobile_number = request.data.get(
                "mobile_number",
                customer.mobile_number,
            )

            customer.email = request.data.get(
                "email",
                customer.email,
            )

            customer.address = request.data.get(
                "address",
                customer.address,
            )

            customer.city = request.data.get(
                "city",
                customer.city,
            )

            customer.state = request.data.get(
                "state",
                customer.state,
            )

            customer.pincode = request.data.get(
                "pincode",
                customer.pincode,
            )

            customer.gst_number = request.data.get(
                "gst_number",
                customer.gst_number,
            )

            customer.customer_type = request.data.get(
                "customer_type",
                customer.customer_type,
            )

            customer.save()

            return success_response(
                CustomerSerializer.serialize(customer),
                Messages.CUSTOMER_UPDATED,
                status.HTTP_200_OK,
            )

        except Exception as e:

            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteCustomerView(AuthenticatedAPIView):

    def delete(self, request, customer_id):

        try:

            customer = Customer.objects(customer_id=customer_id).first()

            if not customer:

                return error_response(
                    Messages.CUSTOMER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            customer.delete()

            return success_response(
                None,
                Messages.CUSTOMER_DELETED,
                status.HTTP_200_OK,
            )

        except Exception as e:

            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MakeCustomerActiveInactiveView(AuthenticatedAPIView):
    def post(self, request, customer_id):
        try:

            customer = Customer.objects(customer_id=customer_id).first()

            if not customer:

                return error_response(
                    Messages.CUSTOMER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )
            statusValue = request.data.get("status")
            if not statusValue:
                return error_response(
                    Messages.CUSTOMER_STATUS_REQUIRED,
                    None,
                    status.HTTP_400_BAD_REQUEST,
                )

            customer.status = statusValue
            customer.save()

            return success_response(
                None,
                Messages.customer_status_updated(statusValue),
                status.HTTP_200_OK,
            )

        except Exception as e:

            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MakeCustomerActiveInactiveView(AuthenticatedAPIView):
    def post(self, request, customer_id):
        try:

            customer = Customer.objects(customer_id=customer_id).first()

            if not customer:

                return error_response(
                    Messages.CUSTOMER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )
            statusValue = request.data.get("status")
            if not statusValue:
                return error_response(
                    Messages.CUSTOMER_STATUS_REQUIRED,
                    None,
                    status.HTTP_400_BAD_REQUEST,
                )

            customer.status = statusValue
            customer.save()

            return success_response(
                None,
                Messages.customer_status_updated(statusValue),
                status.HTTP_200_OK,
            )

        except Exception as e:

            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
