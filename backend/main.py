from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router

from app.core.config import settings
from app.core.logger import logger

import app.core.langsmith

# Application Lifespan

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs during application startup and shutdown.
    """

    logger.info("Starting AI-Powered Study Assistant...")

    # Create upload directory if it doesn't exist
    Path(settings.UPLOAD_DIRECTORY).mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info("Upload directory verified.")
    logger.info("Application startup completed.")

    yield

    logger.info("Application shutdown completed.")


# FastAPI Application

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Study Assistant using LangChain, LangGraph, Gemini, Voyage AI and Qdrant.",
    lifespan=lifespan,
)
# Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers

app.include_router(
    health_router,
    prefix=settings.API_PREFIX,
    tags=["Health"],
)

app.include_router(
    upload_router,
    prefix=settings.API_PREFIX,
    tags=["Upload"],
)

app.include_router(
    chat_router,
    prefix=settings.API_PREFIX,
    tags=["Chat"],
)

# Root Endpoint

@app.get("/", tags=["Root"])
async def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running"
    }