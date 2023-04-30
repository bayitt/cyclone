from fastapi import APIRouter, Request, HTTPException, status
from authlib.integrations.starlette_client import OAuthError
from datetime import datetime, timedelta
from jose import jwt
from os import environ

from ..utilities.oauth import get_oauth_object
from ..schemas.token import Token

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    oauth = get_oauth_object()
    return await oauth.google.authorize_redirect(
        request, environ.get("GOOGLE_CLIENT_REDIRECT")
    )


@router.post("/tokens")
async def generate_token(request: Request) -> Token:
    oauth = get_oauth_object()
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate google credentials",
        )

    user = access_token["userinfo"]

    if user["email"] != environ.get("AUTHORIZED_EMAIL"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this application",
        )

    expires = datetime.utcnow() + timedelta(
        minutes=int(environ.get("JWT_TOKEN_EXPIRES_MINUTES"))
    )
    data = {"sub": environ.get("AUTHORIZED_EMAIL"), "exp": expires}
    token = jwt.encode(data, environ.get("SECRET_KEY"), algorithm="HS256")

    return {"token": token}
