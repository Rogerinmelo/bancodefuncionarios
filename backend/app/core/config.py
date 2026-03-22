from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BNC Funcionarios API"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/bnc_funcionarios"

    jwt_secret_key: str = "change-me"
    jwt_refresh_secret_key: str = "change-me-refresh"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    storage_bucket: str = "bnc-fotos"
    storage_region: str = "us-east-1"
    storage_endpoint_url: str | None = "http://localhost:9000"
    storage_access_key: str | None = "minioadmin"
    storage_secret_key: str | None = "minioadmin"
    storage_use_ssl: bool = False
    max_upload_size_bytes: int = 5 * 1024 * 1024
    allowed_upload_mime_types: str = "image/jpeg,image/png,image/webp"
    signed_url_expires_seconds: int = 3600

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
