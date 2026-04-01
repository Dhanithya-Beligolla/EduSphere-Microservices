from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.routes.info_routes import router as info_router
from app.routes.proxy_routes import router as proxy_router


app = FastAPI(
    title="EduSphere API Gateway",
    version=settings.app_version,
    description=(
        "Single-entry-point API Gateway for EduSphere microservices. "
        "Routes requests to identity, assessment, learning materials, "
        "monitoring, and additional domain services."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(info_router)
app.include_router(proxy_router)


@app.get("/api-docs", include_in_schema=False)
async def api_docs_alias():
    return get_swagger_ui_html(openapi_url="/api-docs.json", title="EduSphere API Gateway Docs")


@app.get("/api-docs.json", include_in_schema=False)
async def api_docs_json_alias():
    return JSONResponse(app.openapi())
