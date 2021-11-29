from fastapi import FastAPI
from container import Container
from src.api import endpoints
from src.api.config.exception_handlers import set_exception_handlers


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    set_exception_handlers(app)

    return app
