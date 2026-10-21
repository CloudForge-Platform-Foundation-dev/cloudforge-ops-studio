from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from src.ops_studio.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="CloudForge Ops Studio - Auto-Healer",
)


@app.get("/health", tags=["health"])
async def health_check():
    """Return service health and version."""
    return {"status": "healthy", "version": settings.app_version}


@app.get("/ready", tags=["health"])
async def readiness_check():
    """Return service readiness."""
    return {"status": "ready"}


@app.get("/live", tags=["health"])
async def liveness_check():
    """Return service liveness."""
    return {"status": "alive"}


@app.get("/", tags=["meta"])
async def root():
    """Return service name, version and status."""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


OWNER = "niphan1000-cyber1000"


def custom_openapi():
    """Build the OpenAPI schema with the metadata Foundation governance requires."""
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        contact={"name": OWNER, "email": "niphan1000@gmail.com"},
        license_info={"name": "MIT", "identifier": "MIT"},
    )
    schema["info"]["x-owner"] = OWNER
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi
