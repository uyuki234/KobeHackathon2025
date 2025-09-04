from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
import os
from .routers.ideas import router as ideas_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    yield
    print("Application shutdown...")

app = FastAPI(title="Idea Canvas Backend",version="0.1.0",lifespan=lifespan)

# router 
app.include_router(ideas_router, prefix="/api")


# CORS 
FRONT_ORIGIN = os.getenv("FRONT_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONT_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status": exc.status_code}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Validation failed", "details": exc.errors()}
    )

