from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.exceptions.exceptions import DatabaseException
from src.domain.exceptions.exceptions import ServiceExceptions
from src.api.exceptions.exceptions import AuthenticationException


def set_exception_handlers(app):
    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request: Request, exc):
        details = [{"field": item['loc'][1], "message": item['msg']}
                   for item in exc.errors()]
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            content=jsonable_encoder({"details": details}))

    @app.exception_handler(DatabaseException)
    def database_exception_handler(request: Request, exc):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(exc))

    @app.exception_handler(ServiceExceptions)
    def service_exception_handler(request: Request, exc: ServiceExceptions):
        return JSONResponse(status_code=exc.status_code, content=jsonable_encoder({"entity": exc.entity, "details": exc.details}))

    return app
