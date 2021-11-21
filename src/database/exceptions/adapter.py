from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from src.database.exceptions.exceptions import UniqueViolationException


def get_exception(entity: str, exception: IntegrityError):
    orig_exc = exception.orig
    if isinstance(orig_exc, UniqueViolation):
        return UniqueViolationException(entity=entity)


def db_exc_adapter(entity: str, exception: Exception):
    if isinstance(exception, IntegrityError):
        return get_exception(entity, exception)
