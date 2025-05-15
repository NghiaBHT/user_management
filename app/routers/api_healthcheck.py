from fastapi import APIRouter

from app.schemas.sche_base import ResponseSchemaBase

router = APIRouter(prefix="/healthcheck", tags=["health-check"]) 

@router.get("", response_model=ResponseSchemaBase)
async def get():
    return {"message": "Health check success"}

