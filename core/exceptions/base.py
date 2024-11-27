from http import HTTPStatus

from starlette.exceptions import HTTPException as StarletteHTTPException


class CustomException(StarletteHTTPException):
    code = HTTPStatus.BAD_GATEWAY
    status_code = HTTPStatus.BAD_GATEWAY
    detail = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, detail=None):
        if detail:
            self.detail = detail


class BadRequestException(CustomException):
    code = HTTPStatus.BAD_REQUEST
    status_code = HTTPStatus.BAD_REQUEST
    detail = HTTPStatus.BAD_REQUEST.description


class NotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    status_code = HTTPStatus.NOT_FOUND
    detail = HTTPStatus.NOT_FOUND.description


class ForbiddenException(CustomException):
    code = HTTPStatus.FORBIDDEN
    status_code = HTTPStatus.FORBIDDEN
    detail = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    status_code = HTTPStatus.UNAUTHORIZED
    detail = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntity(CustomException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    detail = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DatabaseError(CustomException):
    pass


class InternalServerError(CustomException):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    detail = HTTPStatus.INTERNAL_SERVER_ERROR.description
