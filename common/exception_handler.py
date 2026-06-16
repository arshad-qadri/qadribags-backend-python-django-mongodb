from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from common.constants import Messages


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        return Response(
            {
                "success": False,
                "message": Messages.REQUEST_FAILED,
                "errors": response.data
            },
            status=response.status_code
        )

    return Response(
        {
            "success": False,
            "message": Messages.INTERNAL_SERVER_ERROR,
            "errors": str(exc)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
