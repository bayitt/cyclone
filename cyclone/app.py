from fastapi import FastAPI, Depends

from .utilities.env import load_env
from .middleware.session import add_session_middleware
from .routers import auth, application
from .dependencies.auth import auth_guard

load_env()

app = FastAPI()

add_session_middleware(app)

app.include_router(auth.router)
app.include_router(application.router, prefix="/applications", dependencies=[Depends(auth_guard)])
