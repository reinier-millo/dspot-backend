""" Main entry point for the API """
import os
from pathlib import Path
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routes
from app.routes.health import health_router
from app.routes.v1.profile import profile_router
from app.routes.v1.friendship import friendship_router

# Load environment variables
load_dotenv(dotenv_path=f"{Path(__file__).parent}/.env")

# Disable Swagger docs in production
docs_url = "/docs" if os.getenv("ENVIRONMENT") == "development" else None
redoc_url = "/redoc" if os.getenv("ENVIRONMENT") == "development" else None

app = FastAPI(
    title="DSpot API Test",
    description="API for DSpot Test",
    version="0.1.0",
    docs_url=docs_url,
    redoc_url=redoc_url,
)

# Configure CORS
allowed_origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure routes
app.include_router(health_router, prefix="/health")
app.include_router(profile_router, prefix="/v1")
app.include_router(friendship_router, prefix="/v1")
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
