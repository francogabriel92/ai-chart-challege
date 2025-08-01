from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env"),
    )
    OPENAI_API_KEY: str
    TIMEOUT: int = 100  # Default timeout in seconds


# Per docs we can use lru_cache to cache the settings to avoid
# reading the .env file every time.
# See https://fastapi.tiangolo.com/advanced/settings/?h=env#creating-the-settings-only-once-with-lru_cache
@lru_cache
def get_settings():
    return Settings()
