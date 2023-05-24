from fastapi import Header, status
from typing import Annotated
from jose import jwt, JWTError
from os import environ

from ..utilities.exception import CycloneHTTPException


def auth_guard(authorization: Annotated[str | None, Header()] = None):
    auth_exception = CycloneHTTPException(
        error="auth-001",
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not authenticated",
    )

    if not authorization:
        raise auth_exception

    auth_splits = authorization.split(" ")

    if len(auth_splits) != 2:
        raise auth_exception

    token = auth_splits[1]

    try:
        payload = jwt.decode(token, environ.get("SECRET_KEY"), algorithms=["HS256"])
        email: str = payload.get("sub")

        if not email or email != environ.get("AUTHORIZED_EMAIL"):
            raise auth_exception
    except JWTError:
        raise auth_exception
