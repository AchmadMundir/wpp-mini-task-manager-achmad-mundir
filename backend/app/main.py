from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import boards, tasks
from app.core.config import get_settings
from app.core.errors import AppError
from app.core.handlers import (
    app_error_handler,
    database_error_handler,
    http_error_handler,
    request_validation_handler,
    unexpected_error_handler,
)

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="REST API for a board-based mini task manager.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, request_validation_handler)
app.add_exception_handler(StarletteHTTPException, http_error_handler)
app.add_exception_handler(SQLAlchemyError, database_error_handler)
app.add_exception_handler(Exception, unexpected_error_handler)

app.include_router(boards.router)
app.include_router(tasks.router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}

