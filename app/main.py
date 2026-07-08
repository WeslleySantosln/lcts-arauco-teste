from fastapi import FastAPI

from app.api.routes.system import router as system_router
from app.core.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Logistics Control Tower Simulator"
)

app.include_router(system_router)


@app.get("/")
async def root():
    return {
        "project": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running"
    }