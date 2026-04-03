"""
Application configuration loaded from environment variables.
Uses pydantic-settings for typed, validated configuration.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Central application settings."""

    # Application
    app_name: str = Field(default="learning-materials-service")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    # MongoDB
    mongo_uri: str = Field(default="mongodb://localhost:27017")
    mongo_db_name: str = Field(default="lms_learning_materials")

    # JWT
    jwt_secret: str = Field(default="dev-secret-change-in-production")
    jwt_algorithm: str = Field(default="HS256")

    # Feature flags
    enable_agent_features: bool = Field(default=False)

    # Event publisher: "noop" | "log"
    event_publisher: str = Field(default="noop")

    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# Singleton settings instance — import this everywhere
settings = Settings()
