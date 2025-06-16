from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.

    Attributes:
        secret_key (str | None): Secret key for cryptographic operations.
        algorithm (str | None): Algorithm used for token encoding/decoding.
        access_token_expire_minutes (int | None): Token expiration time in minutes.

    """

    secret_key: str | None = None
    algorithm: str | None = None
    access_token_expire_minutes: int | None = None
    admin_username: str
    admin_password: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
