import logging
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """App settings"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_LOG_LEVEL: str

    LLM_API_KEY: str
    LLM_BASE_URL: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore
