from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cors_origins: list[str] = ["http://localhost:5173"]
    log_level: str = "info"

    # LLM — provider-agnostic via Pydantic AI model strings
    anthropic_api_key: str = ""
    llm_model: str = "anthropic:claude-sonnet-4-6"

    # Upload limits
    max_file_size_mb: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_prefix="")


settings = Settings()
