from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.exceptions import ExceptionMiddleware

from api import router
from core.config import config
from core.fastapi.middleware.sqlalchemy import SQLAlchemyMiddleware


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


async def global_exception_handler(request, exc):

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


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Task Manager API",
        description="Create update delete and View your tasks",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        middleware=make_middleware(),
    )
    init_routers(app_=app_)

    return app_


app = create_app()
