from fastapi import APIRouter

from app.schemas.exceptions import UnhealthyDatabaseError
from app.schemas.response import HealthResponse
from core.database.session import test_connection
from core.utils.logging import logger

health_router = APIRouter()


@health_router.get(
    "/",
    summary="Health Check",
    description="Health Check",
    status_code=200,
    responses={
        500: {
            "model": UnhealthyDatabaseError,
            "description": "Database connection failed",
        }
    },
)
async def health_check() -> HealthResponse:
    db_connected = await test_connection()
    if not db_connected:
        logger.error("Database connection failed", exc_info=True)
    return {
        "status": "healthy" if db_connected else "unhealthy",
        "database_connected": db_connected,
    }
