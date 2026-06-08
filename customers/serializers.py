class CustomerSerializer:

    @staticmethod
    def serialize(customer):

        return {
            "id": str(customer.id),
            "customer_id":customer.customer_id,
            "name": customer.name,
            "mobile_number": customer.mobile_number,
            "email": customer.email,
            "address": customer.address,
            "city": customer.city,
            "state": customer.state,
            "pincode": customer.pincode,
            "gst_number": customer.gst_number,
            "customer_type": customer.customer_type,
            "status":customer.status
        }

    @staticmethod
    def serialize_many(customers):

        return [
            CustomerSerializer.serialize(customer)
            for customer in customers
        ]