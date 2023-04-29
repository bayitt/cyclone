from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from os import environ


def get_oauth_object():
    params = {
        "GOOGLE_CLIENT_ID": environ.get("GOOGLE_CLIENT_ID"),
        "GOOGLE_CLIENT_SECRET": environ.get("GOOGLE_CLIENT_SECRET"),
    }
    config = Config(environ=params)
    oauth = OAuth(config)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    return oauth
