from app.core.config import settings

HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]

SERVICE_REGISTRY = {
    "identity": {
        "prefix": "/identity",
        "base_url": settings.identity_service_url,
        "health_path": "/health",
        "display_name": "Identity Service",
    },
    "assessment": {
        "prefix": "/assessment",
        "base_url": settings.homework_service_url,
        "health_path": "/health",
        "display_name": "Homework & Assessment Service",
    },
    "materials": {
        "prefix": "/materials",
        "base_url": settings.learning_materials_service_url,
        "health_path": "/health",
        "display_name": "Learning Materials Service",
    },
    "monitoring": {
        "prefix": "/monitoring",
        "base_url": settings.monitoring_service_url,
        "health_path": "/health",
        "display_name": "Monitoring & Administration Service",
    },
    "academic": {
        "prefix": "/academic",
        "base_url": settings.academic_service_url,
        "health_path": "/api/health",
        "display_name": "Academic Management Service",
    },
    "groups": {
        "prefix": "/groups",
        "base_url": settings.group_service_url,
        "health_path": "/health",
        "display_name": "Group Activities Service",
    },
    "communication": {
        "prefix": "/communication",
        "base_url": settings.communication_service_url,
        "health_path": "/health",
        "display_name": "Communication & Student Support Service",
    },
}
