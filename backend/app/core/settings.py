from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI First CRM HCP Module"
    environment: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./crm_hcp.db"
    groq_api_key: str = "replace_me"
    groq_model: str = "gemma2-9b-it"
    groq_fallback_model: str = "llama-3.3-70b-versatile"
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


settings = Settings()
settings.allowed_origins = ",".join(settings.allowed_origins_list)
