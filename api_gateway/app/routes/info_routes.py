from fastapi import APIRouter

from app.controllers.gateway_controller import (
    downstream_health,
    gateway_health,
    list_registered_routes,
    root_info,
)

router = APIRouter(tags=["Gateway Info"])


@router.get("/", summary="Gateway metadata")
async def get_root_info():
    return await root_info()


@router.get("/health", summary="Gateway health")
async def get_health():
    return await gateway_health()


@router.get("/api/v1/gateway/routes", summary="Registered service routes")
async def get_routes():
    return await list_registered_routes()


@router.get("/api/v1/gateway/services/health", summary="Downstream services health")
async def get_services_health():
    return await downstream_health()
