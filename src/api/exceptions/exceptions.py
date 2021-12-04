from fastapi import status


class AuthenticationException(Exception):
    def __init__(self):
        super().__init__("Token is not valid!")
        self.status_code = status.HTTP_401_UNAUTHORIZED
