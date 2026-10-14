from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import AppError


def error_body(code: str, message: str, field: str | None = None) -> dict:
    body: dict[str, str] = {"error": code, "message": message}
    if field is not None:
        body["field"] = field
    return body


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=error_body(exc.code, exc.message, exc.field),
    )


async def request_validation_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    issue = exc.errors()[0]
    location = issue.get("loc", [])
    field = str(location[-1]) if location else None
    message = issue.get("msg", "Request validation failed")
    return JSONResponse(
        status_code=422,
        content=error_body("VALIDATION_FAILED", message, field),
    )


async def http_error_handler(
    _: Request, exc: StarletteHTTPException
) -> JSONResponse:
    code = "NOT_FOUND" if exc.status_code == 404 else "HTTP_ERROR"
    return JSONResponse(
        status_code=exc.status_code,
        content=error_body(code, str(exc.detail)),
    )


async def database_error_handler(_: Request, __: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=error_body(
            "INTERNAL_ERROR", "A database error occurred. Please try again later."
        ),
    )


async def unexpected_error_handler(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=error_body(
            "INTERNAL_ERROR", "An unexpected error occurred. Please try again later."
        ),
    )

