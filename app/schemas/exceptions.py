from pydantic import BaseModel


class UniqueConstraintViolation(BaseModel):
    error_code: str = "UNPROCESSABLE_ENTITY"
    detail: str = "Unique constraint violation"


class DatabaseError(BaseModel):
    error_code: str = "INTERNAL_SERVER_ERROR"
    detail: str = "Database error occured"


class DatabaseTableError(BaseModel):
    error_code: str = "INTERNAL_SERVER_ERROR"
    detail: str = "Database table does not exists"


class NotFoundError(BaseModel):
    error_code: str = "NOT_FOUND"
    detail: str = "Task with id: 1 does not exist"


class InvalidFormatError(BaseModel):
    error_code: str = "INVALID_FORMAT"
    detail: str = "Expected number, but received string"


class UnhealthyDatabaseError(BaseModel):
    status: str = "unhealthy"
    database_connected: bool = False
