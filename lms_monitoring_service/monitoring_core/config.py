from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "monitoring-administration-service"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    port: int = 4007

    postgres_server: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "monitoring_db"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    database_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
