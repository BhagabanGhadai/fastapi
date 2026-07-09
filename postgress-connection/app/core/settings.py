from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application configuration settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8",extra="ignore")

    PORT: int
    DEBUG: bool
    DB_CONNECTION_STRING: str

settings = Settings()