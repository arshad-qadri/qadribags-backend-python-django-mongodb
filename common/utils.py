from products.models import Product
from customers.models import Customer
from orders.models import Order
from datetime import datetime
import uuid


def generate_sku(category):

    category_map = {
        "School Bags": "SB",
        "Laptop Bags": "LB",
        "Travel Bags": "TB",
        "Duffle Bags": "DB",
    }

    category_code = category_map.get(category, "GEN")

    unique_code = str(uuid.uuid4())[:6].upper()
    count = Product.objects.count() + 1
    return f"QB-{category_code}-{unique_code}-{count:03d}"


def generate_customer_id():
    unique_code = str(uuid.uuid4())[:6].upper()
    count = Customer.objects.count() + 1
    return f"QB-CUST-{unique_code}-{count:03d}"

def generate_order_number():
    unique_code = str(uuid.uuid4())[:6].upper()
    count = Order.objects.count() + 1

    return (
        f"QB-ORD-"
        f"{unique_code}{datetime.now().year}-"
        f"{count:04d}"
    )