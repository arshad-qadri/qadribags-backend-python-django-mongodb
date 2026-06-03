from rest_framework.views import APIView
from rest_framework import status

from common.constants import (
    PRODUCT_CREATED,
    PRODUCT_ALREADY_EXIST,
    ALL_FIELDS_REQUIRED,
    INTERNAL_SERVER_ERROR,
)

from common.response import (
    success_response,
    error_response,
)
from common.utils import generate_sku
from .models import Product


from common.cloudinary_service import (
    upload_image,
)
from .models import ProductImage


class CreateProductView(APIView):

    def post(self, request):
        try:

            name = request.data.get("name")
            category = request.data.get("category")
            sku = generate_sku(category)
            price = request.data.get("price")

            required_fields = [
                "name",
                "category",
                "price",
            ]

            missing_fields = [
                field for field in required_fields if not request.data.get(field)
            ]

            if missing_fields:
                return error_response(
                    ALL_FIELDS_REQUIRED,
                    {"missing_fields": missing_fields},
                    status.HTTP_400_BAD_REQUEST,
                )

            existing_product = Product.objects(sku=sku).first()

            if existing_product:
                return error_response(
                    PRODUCT_ALREADY_EXIST,
                    None,
                    status.HTTP_400_BAD_REQUEST,
                )

            product = Product(
                sku=sku,
                name=name,
                description=request.data.get("description"),
                category=category,
                material=request.data.get("material"),
                colors=request.data.get("colors", []),
                weight=request.data.get("weight"),
                dimensions=request.data.get("dimensions"),
                supplier=request.data.get("supplier"),
                # cost_price=request.data.get("cost_price"),
                price=price,
                stock=request.data.get("stock", 0),
                # status=request.data.get("status", "ACTIVE"),
                images=request.data.get("images", []),
            )

            product.save()

            return success_response(
                {"id": str(product.id)},
                PRODUCT_CREATED,
                status.HTTP_201_CREATED,
            )

        except Exception as e:

            return error_response(
                INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UploadProductImageView(APIView):

    def post(self, request, sku):

        try:
            product = Product.objects(sku=sku).first()

            if not product:
                return error_response(
                    "Product not found",
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            image = request.FILES.get("image")

            if not image:
                return error_response(
                    "Image is required",
                    None,
                    status.HTTP_400_BAD_REQUEST,
                )

            uploaded_image = upload_image(image, f"products/{product.sku}")

            product.images.append(
                ProductImage(
                    public_id=uploaded_image["public_id"],
                    url=uploaded_image["url"],
                )
            )

            product.save()

            return success_response(
                uploaded_image,
                "Image uploaded successfully",
                status.HTTP_200_OK,
            )

        except Exception as e:

            return error_response(
                "Image upload failed",
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetProductBySKU(APIView):
    def post(self, request, sku):
        try:
            product = Product.objects(sku=sku).first()

            return success_response(
                {
                    "sku": product.sku,
                    "name": product.name,
                    "description": product.description,
                    "category": product.category,
                    "material": product.material,
                    "colors": product.colors,
                    "weight": product.weight,
                    "dimensions": product.dimensions,
                    "supplier": product.supplier,
                    "status": product.status,
                    "price": product.price,
                    "stock": product.stock,
                    "images": [
                        {
                            "public_id": image.public_id,
                            "url": image.url,
                        }
                        for image in product.images
                    ],
                    "created_at": product.created_at,
                    "updated_at": product.updated_at,
                },
                "Product found successfully",
                status.HTTP_200_OK,
            )
        except Exception as e:

            return error_response(
                "Image upload failed",
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetProductList(APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            for product in products:
                product["id"] = str(product["id"])

            return success_response(products, None, status.HTTP_200_OK)
        except Exception as e:
            return error_response(
                INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
