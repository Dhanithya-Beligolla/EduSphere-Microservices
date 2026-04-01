from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "lms-api-gateway"
    app_version: str = "1.0.0"
    app_env: str = "development"
    host: str = "0.0.0.0"
    port: int = 8080
    proxy_timeout_seconds: float = 30.0

    identity_service_url: str = Field(default="http://localhost:4001")
    homework_service_url: str = Field(default="http://localhost:4002")
    learning_materials_service_url: str = Field(default="http://localhost:4004")
    monitoring_service_url: str = Field(default="http://localhost:4007")

    academic_service_url: str = Field(default="http://localhost:4003")
    group_service_url: str = Field(default="http://localhost:4006")
    communication_service_url: str = Field(default="http://localhost:4005")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
