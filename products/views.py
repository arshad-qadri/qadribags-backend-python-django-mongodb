from rest_framework import status

from common.authentication import AuthenticatedAPIView
from common.constants import Messages

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
from .serializers import ProductSerializer


class CreateProductView(AuthenticatedAPIView):

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
                    Messages.ALL_FIELDS_REQUIRED,
                    {"missing_fields": missing_fields},
                    status.HTTP_400_BAD_REQUEST,
                )

            existing_product = Product.objects(sku=sku).first()

            if existing_product:
                return error_response(
                    Messages.PRODUCT_ALREADY_EXIST,
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
                Messages.PRODUCT_CREATED,
                status.HTTP_201_CREATED,
            )

        except Exception as e:

            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UploadProductImageView(AuthenticatedAPIView):

    def post(self, request, sku):

        try:
            product = Product.objects(sku=sku).first()

            if not product:
                return error_response(
                    Messages.PRODUCT_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            image = request.FILES.get("image")

            if not image:
                return error_response(
                    Messages.IMAGE_REQUIRED,
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
                Messages.IMAGE_UPLOADED,
                status.HTTP_200_OK,
            )

        except Exception as e:

            return error_response(
                Messages.IMAGE_UPLOAD_FAILED,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetProductBySKU(AuthenticatedAPIView):
    def get(self, request, sku):
        try:
            product = Product.objects(sku=sku).first()

            if not product:
                return error_response(
                    Messages.PRODUCT_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            return success_response(
                ProductSerializer(product).data,
                Messages.PRODUCT_FOUND,
                status.HTTP_200_OK,
            )
        except Exception as e:

            return error_response(
                Messages.IMAGE_UPLOAD_FAILED,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetProductList(AuthenticatedAPIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)

            return success_response(serializer.data, None, status.HTTP_200_OK)
        except Exception as e:
            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ActiveInactiveProductBySKU(AuthenticatedAPIView):
    def post(self, request, sku):
        try:
            requested_status = request.data.get("status")

            if not requested_status:
                return error_response(
                    Messages.STATUS_REQUIRED, None, status.HTTP_400_BAD_REQUEST
                )

            try:
                product = Product.objects.get(sku=sku)
            except Product.DoesNotExist:
                return error_response(
                    Messages.PRODUCT_NOT_FOUND, None, status.HTTP_404_BAD_REQUEST
                )

            product.status = requested_status
            product.save()

            return success_response(
                None, Messages.product_status_updated(requested_status)
            )

        except Exception as e:
            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdateProductView(AuthenticatedAPIView):
    def patch(self, request, sku):
        try:
            try:
                product = Product.objects.get(sku=sku)
            except Product.DoesNotExist:
                return error_response(
                    Messages.PRODUCT_NOT_FOUND, None, status.HTTP_404_NOT_FOUND
                )

            data = request.data

            for field in ["name", "category", "price"]:
                if field in data and not data.get(field):
                    return error_response(
                        Messages.field_cannot_be_empty(field),
                        None,
                        status.HTTP_400_BAD_REQUEST,
                    )

            if "name" in data:
                product.name = data.get("name")
            if "category" in data:
                product.category = data.get("category")
            if "price" in data:
                product.price = data.get("price")
            if "description" in data:
                product.description = data.get("description")
            if "material" in data:
                product.material = data.get("material")
            if "colors" in data:
                product.colors = data.get("colors")
            if "weight" in data:
                product.weight = data.get("weight")
            if "dimensions" in data:
                product.dimensions = data.get("dimensions")
            if "supplier" in data:
                product.supplier = data.get("supplier")
            if "stock" in data:
                product.stock = data.get("stock")
            # if "images" in data:
            #     product.images = data.get("images")

            product.save()

            return success_response(
                {"sku": product.sku},
                Messages.PRODUCT_UPDATED,
                status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteImageView(AuthenticatedAPIView):

    def delete(self, request, sku):
        try:
            public_id = request.data.get("public_id")

            if not public_id:
                return error_response(
                    Messages.MISSING_PUBLIC_ID,
                    Messages.PUBLIC_ID_REQUIRED,
                    status.HTTP_400_BAD_REQUEST,
                )

            product = Product.objects.get(sku=sku)

            # Check if image exists (using object attribute, not dict get)
            image_exists = any(img.public_id == public_id for img in product.images)

            if not image_exists:
                return error_response(
                    Messages.IMAGE_NOT_FOUND,
                    Messages.image_not_associated_with_product(public_id),
                    status.HTTP_404_NOT_FOUND,
                )

            # Filter out the image with the given public_id
            filtered_product_images = [
                img for img in product.images if img.public_id != public_id
            ]
            product.images = filtered_product_images
            product.save()

            return success_response(
                None,
                Messages.IMAGE_DELETED,
                status.HTTP_200_OK,
            )

        except Product.DoesNotExist:
            return error_response(
                Messages.PRODUCT_NOT_FOUND,
                Messages.no_product_found_with_sku(sku),
                status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
