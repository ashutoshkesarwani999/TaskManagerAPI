from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.exceptions import ExceptionMiddleware
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from api import router
from core.config import config
from core.fastapi.middleware.sqlalchemy import SQLAlchemyMiddleware
from core.security.limiter import limiter
from starlette.middleware.base import BaseHTTPMiddleware


csp_policy = "default-src 'self';"
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."},
    )


def init_routers(app_: FastAPI) -> None:
    """
    Initialize FastAPI application routes.
    """
    app_.include_router(router)


async def global_exception_handler(request, exc):
    """
    Global exception handler for the FastAPI application.

    Args:
        request: The incoming request
        exc: The exception that was raised

    Returns:
        JSONResponse: A JSON response containing error details
            - For StarletteHTTPException: Returns the status code and error detail
            - For other exceptions: Returns 500 Internal Server Error
    """
    if isinstance(exc, StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"},
    )


def make_middleware() -> List[Middleware]:
    """
    Configure and create middleware stack for the FastAPI application.

    Returns:
        List[Middleware]: A list of middleware configurations including:
            - CORS middleware with all origins allowed
            - Exception handling middleware
            - SQLAlchemy session middleware
    """
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(ExceptionMiddleware, handlers={Exception: global_exception_handler}),
        Middleware(SQLAlchemyMiddleware),
    ]
    return middleware

def CSPMiddleware(BaseHTTPMiddleware):
    def __init__(self, app,csp_policy):
        super().__init__(app)
        self.csp_policy = csp_policy
    async def dispatch(self,request:Request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = self.csp_policy
        return response

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app_ = FastAPI(
        title="Task Manager API",
        description="Create update delete and View your tasks",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        middleware=make_middleware(),
    )
    app_.add_middleware(CSPMiddleware,csp_policy=csp_policy)
    app_.add_exception_handler(RateLimitExceeded, rate_limit_handler)
    app_.state.limiter = limiter
    app_.add_middleware(SlowAPIMiddleware)
    init_routers(app_=app_)

    return app_


app = create_app()
