from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cors_origins: list[str] = ["http://localhost:5173"]
    log_level: str = "info"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="")


settings = Settings()
