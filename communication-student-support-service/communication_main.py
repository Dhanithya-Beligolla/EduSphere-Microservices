from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from communication_routers import (
    communication_notices,
    communication_messages,
    communication_alerts,
    communication_support_cases
)

app = FastAPI(
    title="Communication & Student Support Service",
    description="Service 05 for LMS - Handling notices, messaging, alerts, and counselling.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- Middleware ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---

# Grouping all under /api/v1 as per requirement
app.include_router(communication_notices.router, prefix="/api/v1")
app.include_router(communication_messages.router, prefix="/api/v1")
app.include_router(communication_alerts.router, prefix="/api/v1")
app.include_router(communication_support_cases.router, prefix="/api/v1")

# --- Default Endpoints ---

@app.get("/", tags=["General"])
async def root():
    """
    Service information.
    """
    return {
        "service": "Communication & Student Support Service",
        "version": "v1",
        "description": "Enterprise-level microservice for school communication."
    }

@app.get("/health", tags=["General"])
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "communication-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
