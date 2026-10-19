from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.ops_studio.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="CloudForge Ops Studio - Auto-Healer",
)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.app_version}


@app.get("/ready")
async def readiness_check():
    return {"status": "ready"}


@app.get("/live")
async def liveness_check():
    return {"status": "alive"}


@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }