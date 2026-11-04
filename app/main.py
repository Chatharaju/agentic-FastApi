from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.api.routes.customers import router as customers_router
# from app.api.routes.jobs import router as jobs_router
from app.api.routes.leads import router as leads_router
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(chat_router)
# app.include_router(jobs_router)
app.include_router(customers_router)
app.include_router(leads_router)


@app.get("/")
async def root():
    return {
        "message": "Agentic AI API is running"
    }