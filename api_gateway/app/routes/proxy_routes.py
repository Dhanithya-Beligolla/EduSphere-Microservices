from fastapi import APIRouter, Request

from app.controllers.gateway_controller import proxy_to_service
from app.core.constants import HTTP_METHODS

router = APIRouter(tags=["Service Proxy"])


@router.api_route("/identity", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/identity/{path:path}", methods=HTTP_METHODS, summary="Proxy -> Identity Service")
async def proxy_identity(request: Request, path: str = ""):
    return await proxy_to_service(request, "identity", path)


@router.api_route("/assessment", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/assessment/{path:path}", methods=HTTP_METHODS, summary="Proxy -> Homework & Assessment Service")
async def proxy_assessment(request: Request, path: str = ""):
    return await proxy_to_service(request, "assessment", path)


@router.api_route("/materials", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/materials/{path:path}", methods=HTTP_METHODS, summary="Proxy -> Learning Materials Service")
async def proxy_materials(request: Request, path: str = ""):
    return await proxy_to_service(request, "materials", path)


@router.api_route("/monitoring", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/monitoring/{path:path}", methods=HTTP_METHODS, summary="Proxy -> Monitoring & Administration Service")
async def proxy_monitoring(request: Request, path: str = ""):
    return await proxy_to_service(request, "monitoring", path)


@router.api_route("/academic", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/academic/{path:path}", methods=HTTP_METHODS, summary="Proxy -> Academic Management Service")
async def proxy_academic(request: Request, path: str = ""):
    return await proxy_to_service(request, "academic", path)


@router.api_route("/groups", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/groups/{path:path}", methods=HTTP_METHODS, summary="Proxy -> Group Activities Service")
async def proxy_groups(request: Request, path: str = ""):
    return await proxy_to_service(request, "groups", path)


@router.api_route("/communication", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/communication/{path:path}", methods=HTTP_METHODS, summary="Proxy -> Communication & Student Support Service")
async def proxy_communication(request: Request, path: str = ""):
    return await proxy_to_service(request, "communication", path)
