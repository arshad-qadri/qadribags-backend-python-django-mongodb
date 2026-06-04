import jwt
from django.conf import settings
from rest_framework.exceptions import APIException, AuthenticationFailed, NotFound
from rest_framework.views import APIView

from common.constants import TOKEN_EXPIRED, TOKEN_REQUIRED, USER_NOT_FOUND
from users.models import User


class TokenRequired(APIException):
    status_code = 401
    default_detail = TOKEN_REQUIRED
    default_code = "not_authenticated"


class AuthenticatedAPIView(APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if request.method == "OPTIONS":
            return

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise TokenRequired()

        token_parts = auth_header.split(" ")

        if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
            raise AuthenticationFailed("Invalid token")

        try:
            payload = jwt.decode(
                token_parts[1],
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )
            user = User.objects(id=payload.get("user_id")).first()

            if not user:
                raise NotFound(USER_NOT_FOUND)

            request.auth_user = user

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(TOKEN_EXPIRED)
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
