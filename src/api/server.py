from fastapi import FastAPI
from container import Container
from src.api.config.exception_handlers import set_exception_handlers
from src.api.config.middlewares import set_middlewares
from src.api.endpoints import register_routes


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container
    set_exception_handlers(app)
    set_middlewares(app)
    register_routes(app)

    return app
