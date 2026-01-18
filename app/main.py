from fastapi import FastAPI

from app.api.v1 import auth
from app.api.v1 import org
from app.api.v1 import project

from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
import app.models 
from app.core.logging import setup_logging
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler
)
setup_logging()


app = FastAPI(title="My FastAPI Application")

app.include_router(auth.router)
app.include_router(org.router)
app.include_router(project.router)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}
