from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from app.routers import api_auth, api_healthcheck, api_user
from app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(title="User Managerment")
    app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    app.include_router(api_healthcheck.router)
    app.include_router(api_user.router)
    app.include_router(api_auth.router)
    return app

app = create_app()