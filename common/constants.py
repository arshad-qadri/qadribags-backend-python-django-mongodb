class Messages:
    SUCCESS = "Success"
    SOMETHING_WENT_WRONG = "Something went wrong"
    BAD_REQUEST = "Bad Request"
    REQUEST_FAILED = "Request failed"
    INTERNAL_SERVER_ERROR = "Internal server error"

    EMAIL_ALREADY_EXIST = "Email already exist"
    LOGIN_SUCCESS = "Login successfully"
    INVALID_TOKEN = "Invalid token"
    TOKEN_EXPIRED = "Token expired"
    TOKEN_REQUIRED = "Token is required"
    USERNAME_ALREADY_EXIST = "Username already exist"
    USER_FETCHED = "User fetched successfully"
    USER_CREATED = "User created successfully"
    USER_UPDATED = "User updated successfully"
    USER_DELETED = "User deleted successfully"
    USER_NOT_FOUND = "User not found"
    USER_ALREADY_EXISTS = "User already exists"
    INVALID_CREDENTIALS = "Invalid credentials"
    ALL_FIELDS_REQUIRED = "All fields are required"

    PRODUCT_CREATED = "Product created successfully"
    PRODUCT_ALREADY_EXIST = "Product already exists"
    PRODUCT_NOT_FOUND = "Product not found"
    PRODUCT_FOUND = "Product found successfully"
    PRODUCT_UPDATED = "Product updated successfully"
    PRODUCT_COUNT_FETCHED = "Product count fetched successfully"
    IMAGE_REQUIRED = "Image is required"
    IMAGE_UPLOADED = "Image uploaded successfully"
    IMAGE_UPLOAD_FAILED = "Image upload failed"
    IMAGE_NOT_FOUND = "Image not found"
    IMAGE_DELETED = "Image deleted successfully"
    MISSING_PUBLIC_ID = "Missing public_id"
    PUBLIC_ID_REQUIRED = "public_id is required in request body"
    STATUS_REQUIRED = "Status is required"

    CUSTOMER_CREATED = "Customer created successfully"
    CUSTOMER_ALREADY_EXIST = "Customer already exists"
    CUSTOMER_NOT_FOUND = "Customer not found"
    CUSTOMER_DELETED = "Customer deleted successfully"
    CUSTOMERS_FETCHED = "Customers fetched successfully"
    CUSTOMER_FETCHED = "Customer fetched successfully"
    CUSTOMER_UPDATED = "Customer updated successfully"
    CUSTOMER_STATUS_REQUIRED = "Status field is required"
    CUSTOMER_ORDER_DATA_FETCHED = "Fetched customer order data successfully"
    CUSTOMER_ORDER_VALUE_FETCHED = "Fetched customer order value successfully"

    ORDER_CREATED = "Order created successfully"
    ORDER_NOT_FOUND = "Order not found"
    ORDER_UPDATED = "Order updated successfully."
    ORDERS_FETCHED = "Orders fetched successfully."
    ORDER_FETCHED = "Order fetched successfully."
    ORDER_ITEMS_REQUIRED = "Order items are required"
    ORDER_ITEM_REQUIRED = "At least one order item is required"
    NEW_ITEMS_NOT_ALLOWED_ON_ORDER_EDIT = "New items cannot be added while editing an order"
    SKU_AND_QUANTITY_REQUIRED = "Sku and quantity are required"
    QUANTITY_MUST_BE_POSITIVE = "Quantity must be greater than zero"
    AMOUNT_PAYING_INVALID = "amount_paying must be a valid number"
    AMOUNT_PAYING_NEGATIVE = "amount_paying cannot be negative"
    AMOUNT_PAYING_EXCEEDS_TOTAL = "amount_paying cannot be greater than grand total"

    INSUFFICIENT_STOCK = "Insufficient stock"
    STOCK_FETCHED = "Stock fetched successfully"
    LOW_STOCK_PRODUCT_COUNT_FETCHED = "Low stock product count fetched successfully"
    CATALOG_VALUE_FETCHED = "Catalog value fetched successfully"
    LOW_STOCK_ALERTS_FETCHED = "Low stock alerts fetched successfully"

    @classmethod
    def customer_status_updated(cls, status_value):
        return f"{status_value.capitalize()} customer status successfully updated"

    @classmethod
    def product_status_updated(cls, requested_status):
        return f"Product {requested_status.lower()} successfully"

    @classmethod
    def field_cannot_be_empty(cls, field_name):
        return f"{field_name.capitalize()} cannot be empty"

    @classmethod
    def product_not_found_for_sku(cls, sku):
        return f"Product not found for sku {sku}"

    @classmethod
    def image_not_associated_with_product(cls, public_id):
        return (
            f"The image with public_id '{public_id}' is not associated with this product."
        )

    @classmethod
    def no_product_found_with_sku(cls, sku):
        return f"No product found with SKU: {sku}"
