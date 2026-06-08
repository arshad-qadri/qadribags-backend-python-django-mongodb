from mongoengine import (
    Document,
    StringField,
    EmailField,
    DateTimeField,
)

from datetime import datetime


class Customer(Document):

    name = StringField(
        required=True,
        max_length=100,
    )

    mobile_number = StringField(
        required=True,
        unique=True,
    )
    
    customer_id = StringField()

    email = EmailField()

    address = StringField()

    city = StringField()

    state = StringField()

    pincode = StringField()

    gst_number = StringField()
    
    status = StringField(default="ACTIVE", choices=["ACTIVE", "INACTIVE"])

    customer_type = StringField(
        default="RETAIL",
        choices=[
            "RETAIL",
            "WHOLESALE",
            "DISTRIBUTOR",
        ],
    )

    created_at = DateTimeField(
        default=datetime.utcnow
    )

    meta = {
        "collection": "customers"
    }