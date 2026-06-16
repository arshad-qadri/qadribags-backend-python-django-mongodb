from rest_framework.exceptions import APIException
from common.constants import Messages


class BadRequestException(APIException):
    status_code = 400
    default_detail = Messages.BAD_REQUEST
