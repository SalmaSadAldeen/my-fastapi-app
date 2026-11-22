import os
from fastapi import FastAPI
from fastapi import HTTPException
from app.routers import items

tags_metadata = [
    {"name": "meta", "description": "Service info and health checks."},
    {
        "name": "items",
        "description": "Create, read, update and delete items (stored in memory).",
    },
]
APP_NAME = os.getenv("APP_NAME", "FastAPI DevOps Service")
APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "Welcome to FastAPI")
API_SECRET = os.getenv("API_SECRET", "")

app = FastAPI(
    title=APP_NAME,
    description="A minimal FastAPI backend with in-memory storage (no database).",
    version=APP_VERSION,
    openapi_tags=tags_metadata,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc (alternative docs)
    openapi_url="/openapi.json",  # Raw OpenAPI schema
    swagger_ui_parameters={
        "docExpansion": "list",
        "defaultModelsExpandDepth": 1,
        "tryItOutEnabled": True,
        "displayRequestDuration": True,
    },
)

app.include_router(items.router)


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    return {"message": WELCOME_MESSAGE, "docs": "/docs"}


@app.get("/health", tags=["meta"])
def health() :
    raise HTTPException(status_code=500, detail="Broken health check")


@app.get("/config", tags=["meta"])
def config() -> dict[str, object]:
    return {
        "app_name": APP_NAME,
        "app_env": APP_ENV,
        "app_version": APP_VERSION,
        "welcome_message": WELCOME_MESSAGE,
        "api_secret_configured": bool(API_SECRET.strip()),
    }
