from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and 'data' in response:
        response.data['code'] = exc.code if hasattr(exc, 'code') else "UNKNOWN_ERROR"
        response.data['message'] = exc.detail if hasattr(exc, 'detail') else "Unknown Error Occurred"
        if 'detail' in response.data:
            del response.data['detail']

    return response


class APIError(APIException):

    default_detail = 'An unknown error occurred.'
    default_code = 'UNKNOWN_ERROR'
    default_status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=default_detail, code=default_code, status_code=default_status_code):
        self.detail = detail
        self.code = code
        self.status_code = status_code


class AuthError(Exception):
    def __init__(self, message, code=None):
        if code:
            self.code = code
        self.message = message
        super().__init__(message)


class PermissionDenied(Exception):
    def __init__(self, message, code=None):
        if code:
            self.code = code
        self.message = message
        super().__init__(message)


__all__ = [
    "APIError",
    "AuthError",
    "PermissionDenied"
]