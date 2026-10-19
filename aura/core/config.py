from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AURA"
    log_level: str = "INFO"
    max_upload_mb: int = 20
    chunk_size: int = 900
    chunk_overlap: int = 150

    model_config = SettingsConfigDict(env_prefix="AURA_", env_file=".env", extra="ignore")


settings = Settings()
