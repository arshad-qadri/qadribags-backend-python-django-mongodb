from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings
from common.constants import Messages
from common.response import error_response, success_response

from .models import User


class RegisterView(APIView):

    def post(self, request):
        try:

            name = request.data.get("name")
            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")

            if not name or not username or not email or not password:
                return error_response(
                    Messages.ALL_FIELDS_REQUIRED, None, status.HTTP_400_BAD_REQUEST
                )

            existing_user = User.objects(username=username).first()

            if existing_user:
                return error_response(
                    Messages.USERNAME_ALREADY_EXIST, None, status.HTTP_400_BAD_REQUEST
                )

            existing_email = User.objects(email=email).first()
            if existing_email:
                return error_response(
                    Messages.EMAIL_ALREADY_EXIST, None, status.HTTP_400_BAD_REQUEST
                )

            user = User(
                name=name,
                username=username,
                email=email,
                password=make_password(password),
            )

            user.save()

            return success_response(None, Messages.USER_CREATED, status.HTTP_201_CREATED)

        except Exception as e:

            return error_response(
                Messages.INTERNAL_SERVER_ERROR, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):

    def post(self, request):
        try:

            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return error_response(
                    Messages.ALL_FIELDS_REQUIRED,
                    None,
                    status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects(username=username).first()

            if not user:
                return error_response(
                    Messages.INVALID_CREDENTIALS,
                    None,
                    status.HTTP_401_UNAUTHORIZED,
                )

            is_valid_password = check_password(
                password,
                user.password,
            )

            if not is_valid_password:
                return error_response(
                    Messages.INVALID_CREDENTIALS,
                    None,
                    status.HTTP_401_UNAUTHORIZED,
                )

            access_token = jwt.encode(
                {
                    "user_id": str(user.id),
                    "username": user.username,
                    "exp": datetime.now(timezone.utc) + timedelta(hours=24),
                },
                settings.SECRET_KEY,
                algorithm="HS256",
            )

            return success_response(
                {
                    "access_token": access_token,
                    # "user": {
                    #     "id": str(user.id),
                    #     "username": user.username,
                    #     "email": user.email,
                    #     "role": user.role,
                    # },
                },
                Messages.LOGIN_SUCCESS,
                status.HTTP_200_OK,
            )

        except Exception as e:

            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetLoggedInUser(APIView):

    def get(self, request):
        try:

            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return error_response(
                    Messages.TOKEN_REQUIRED,
                    None,
                    status.HTTP_401_UNAUTHORIZED,
                )

            token = auth_header.split(" ")[1]

            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )

            user_id = payload["user_id"]

            user = User.objects(id=user_id).first()

            if not user:
                return error_response(
                    Messages.USER_NOT_FOUND,
                    None,
                    status.HTTP_404_NOT_FOUND,
                )

            return success_response(
                {
                    "id": str(user.id),
                    "name":user.name,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
                Messages.USER_FETCHED,
                status.HTTP_200_OK,
            )

        except jwt.ExpiredSignatureError:

            return error_response(
                Messages.TOKEN_EXPIRED,
                None,
                status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            print(e)
            return error_response(
                Messages.INTERNAL_SERVER_ERROR,
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
