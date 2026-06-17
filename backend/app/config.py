from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "CompliancePilot AI"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str = "postgresql://compliance:compliance123@localhost:5432/compliancepilot"
    secret_key: str = "change-me-in-production-use-openssl-rand-hex-32"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    chroma_persist_dir: str = "./data/chroma"
    upload_dir: str = "./data/uploads"
    report_dir: str = "./data/reports"

    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    tesseract_cmd: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def chroma_path(self) -> Path:
        return Path(self.chroma_persist_dir)

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir)

    @property
    def report_path(self) -> Path:
        return Path(self.report_dir)


@lru_cache
def get_settings() -> Settings:
    return Settings()
