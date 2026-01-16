from fastapi import FastAPI
from app.api.v1 import auth
from app.api.v1 import org
import app.models 
app = FastAPI(title="My FastAPI Application")
app.include_router(auth.router)
app.include_router(org.router)
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}
