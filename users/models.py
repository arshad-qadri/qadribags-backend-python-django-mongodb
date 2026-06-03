from mongoengine import Document
from mongoengine import StringField
from mongoengine import EmailField


class User(Document):
    name = StringField(
        required=True,
    )
    username = StringField(
        required=True,
        unique=True
    )

    email = EmailField(
        required=True,
        unique=True
    )

    password = StringField(
        required=True
    )

    role = StringField(
        default="ADMIN"
    )

    meta = {
        "collection": "users"
    }