from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  app_name: str = "SANKALP API"
  app_env: str = "development"
  app_debug: bool = True

  database_url: str

  frontend_url: str = "http://localhost:5173"

  ai_provider: str = "mock"
  ai_model: str = "gpt-5-mini"
  ai_api_key: str | None = None

  model_config = SettingsConfigDict(
    env_file=[
      Path(__file__).resolve().parents[1] / "api" / ".env",
      Path(__file__).resolve().parents[2] / ".env",
      Path(__file__).resolve().parents[3] / ".env",
    ],
    extra="ignore",
  )

settings = Settings()