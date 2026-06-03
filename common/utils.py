from products.models import Product
import uuid

def generate_sku(category):

    category_map = {
        "School Bags": "SB",
        "Laptop Bags": "LB",
        "Travel Bags": "TB",
        "Duffle Bags": "DB",
    }

    category_code = category_map.get(
        category,
        "GEN"
    )

    unique_code = str(uuid.uuid4())[:6].upper()
    count = Product.objects.count() + 1
    return f"QB-{category_code}-{unique_code}-{count:03d}"