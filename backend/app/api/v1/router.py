from fastapi import APIRouter

from app.api.v1.routes import hcps, interactions, system

api_router = APIRouter()
api_router.include_router(system.router, tags=["system"])
api_router.include_router(hcps.router, prefix="/hcps", tags=["hcps"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["interactions"])
