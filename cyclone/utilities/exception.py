from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class CycloneHTTPException(StarletteHTTPException):
    def __init__(
        self,
        error: str,
        status_code: int,
        detail: str | None = "An error occured",
        headers: dict | None = None,
    ):
        self.error = error
        super().__init__(status_code=status_code, detail=detail, headers=headers)


def register_http_exception_handler(app: FastAPI):
    @app.exception_handler(CycloneHTTPException)
    def http_exception_handler(request: Request, exception: CycloneHTTPException):
        return JSONResponse(
            status_code=exception.status_code,
            content={"error": exception.error, "message": exception.detail},
        )
