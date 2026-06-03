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
from datetime import datetime


class ProductImage(EmbeddedDocument):

    public_id = StringField(required=True)

    url = StringField(required=True)


class Product(Document):

    sku = StringField(required=True, unique=True)

    name = StringField(required=True, max_length=200)

    description = StringField()

    category = StringField(required=True)

    material = StringField()

    colors = ListField(StringField(), default=[])

    weight = FloatField()

    dimensions = StringField()

    supplier = StringField()

    status = StringField(default="ACTIVE", choices=["ACTIVE", "INACTIVE"])

    price = FloatField(required=True)

    stock = IntField(default=0)

    images = ListField(EmbeddedDocumentField(ProductImage))

    created_at = DateTimeField(default=datetime.utcnow)

    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "products"}
