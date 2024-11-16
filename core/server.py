from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from api import router
from core.config import config
from core.fastapi.middleware.sqlalchemy import SQLAlchemyMiddleware

def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)



def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(SQLAlchemyMiddleware)
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