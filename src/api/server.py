from fastapi import FastAPI
from container import Container
from src.api import endpoints
from src.api.config.exception_handlers import set_exception_handlers
from src.api.config.middlewares import set_middlewares


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    app = set_exception_handlers(app)
    app = set_middlewares(app)

    return app
