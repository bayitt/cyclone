from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from os import environ


def add_session_middleware(app: FastAPI):
    app.add_middleware(SessionMiddleware, secret_key=environ.get("SECRET_KEY"))
