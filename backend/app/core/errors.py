from typing import Any, Optional
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel


class ErrorBody(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None


def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    body = ErrorBody(
        code="validation_error",
        message="Request is invalid",
        details=exc.errors()
    )
    return JSONResponse(status_code=400, content={"error": body.model_dump()})
