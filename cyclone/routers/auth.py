from fastapi import APIRouter, Request
from os import environ

from ..utilities.oauth import get_oauth_object

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    oauth = get_oauth_object()
    return await oauth.google.authorize_redirect(
        request, environ.get("GOOGLE_CLIENT_REDIRECT")
    )
