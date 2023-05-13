from fastapi import FastAPI, Depends, Request, Response

from .utilities.env import load_env
from .middleware.session import add_session_middleware
from .routers import auth, application, credentials
from .dependencies.auth import auth_guard
from .database.setup import SessionLocal

load_env()

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)

    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()

    return response


add_session_middleware(app)

app.include_router(auth.router)
app.include_router(
    application.router, prefix="/applications", dependencies=[Depends(auth_guard)]
)
app.include_router(
    credentials.router, prefix="/credentials", dependencies=[Depends(auth_guard)]
)
