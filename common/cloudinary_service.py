import cloudinary
import cloudinary.uploader

from django.conf import settings


cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_image(file, folder="products"):

    result = cloudinary.uploader.upload(
        file,
        folder=folder,
    )

    return {
        "public_id": result["public_id"],
        "url": result["secure_url"],
    }


def delete_image(public_id):

    return cloudinary.uploader.destroy(
        public_id
    )