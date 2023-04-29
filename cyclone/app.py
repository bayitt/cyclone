from fastapi import FastAPI

from .utilities.env import load_env
from .middleware.session import add_session_middleware
from .routers import auth

load_env()

app = FastAPI()

add_session_middleware(app)

app.include_router(auth.router)
