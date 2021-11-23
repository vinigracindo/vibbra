from rest_framework import exceptions, status


class Conflict(exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, detail=None, code=None):
        super().__init__(detail=detail, code=code)
