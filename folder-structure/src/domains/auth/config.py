from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    jwt_secret: str = "change-me-via-JWT_SECRET-env-var-not-secure"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


auth_settings = AuthSettings()
