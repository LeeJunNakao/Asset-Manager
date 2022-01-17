from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import jwt
from src.config import JWT_SECRET
from src.api.exceptions.exceptions import AuthenticationException


def set_middlewares(app):
    @app.middleware("http")
    async def check_token(request: Request, call_next):
        try:
            token = request.headers.get("access_token")
            if not token:
                raise AuthenticationException()

            header_user_id = int(request.headers.get("user_id"))
            decoded_jwt = jwt.decode(token, JWT_SECRET, algorithms="HS256")
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", decoded_jwt)
            user_id = int(decoded_jwt["data"].get("id"))

            if header_user_id and header_user_id != user_id:
                raise AuthenticationException()

            response = await call_next(request)

            return response
        except Exception as exc:
            return JSONResponse(status_code=401, content=jsonable_encoder({"details": "Credentials invalid"}))

    return app
