from datetime import datetime

from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    StringField,
    FloatField,
    IntField,
    DateTimeField,
)

class OrderItem(EmbeddedDocument):

    sku = StringField(required=True)

    quantity = IntField(required=True)

class Order(Document):

    order_number = StringField(
        required=True,
        unique=True
    )

    customer_id = StringField(
        required=True
    )

    items = ListField(
        EmbeddedDocumentField(OrderItem)
    )

    grand_total = FloatField(
        required=True
    )

    paid_amount = FloatField(
        default=0
    )

    payment_type = StringField(
        default="CREDIT"
    )

    payment_mode = StringField(
        default=""
    )

    due_amount = FloatField(
        required=True
    )

    payment_status = StringField(
        default="UNPAID"
    )

    status = StringField(
        default="CONFIRMED"
    )

    created_at = DateTimeField(
        default=datetime.utcnow
    )

    meta = {
        "collection": "orders"
    }
