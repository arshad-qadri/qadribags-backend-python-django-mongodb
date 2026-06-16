from rest_framework.response import Response
from common.constants import Messages


def success_response(
    data=None,
    message=Messages.SUCCESS,
    status_code=200
):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data
        },
        status=status_code
    )


def error_response(
    message=Messages.SOMETHING_WENT_WRONG,
    errors=None,
    status_code=400
):
    return Response(
        {
            "success": False,
            "message": message,
            "errors": errors
        },
        status=status_code
    )
