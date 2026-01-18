from fastapi import HTTPException, status 
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from typing import Any  , Optional

class CustomException:
    def __init__(self , message : str , status_code : int  ,  details : Optional[Any] = None):
        self.status_code = status_code
        self.message = message
        self.details = details
    def to_response(self) -> JSONResponse:
        return {
            "status_code": self.status_code,
            "message": self.message,
            "details": self.details
        }

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=CustomException(
            message=str(exc.detail),
            status_code=f"HTTP_{exc.status_code}",
            details=None
        ).to_response(),
    )
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"]) if error["loc"] else "unknown"
        msg = error["msg"]
        errors.append(f"{field}: {msg}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=CustomException(
            message="input validation error",
            status_code="VALIDATION_ERROR",
            details=errors
        ).to_response(),
    )
async def global_exception_handler(request: Request, exc: Exception):  
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=CustomException(
            message="internal server error",
            status_code ="INTERNAL_SERVER_ERROR",
            details=str(exc) 
        ).to_response(),
    )