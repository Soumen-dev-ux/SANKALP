from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator

class Settings(BaseSettings):
  app_name: str = "SANKALP API"
  app_env: str = "development"
  app_debug: bool = True

  database_url: str = "sqlite:///./sankalp.db"

  frontend_url: str = "http://localhost:5173"
  cors_allowed_origins: str = "http://localhost:5173"

  @property
  def cors_origins_list(self) -> list[str]:
      return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

  ai_provider: str = "mock"
  ai_model: str = "gpt-5-mini"
  ai_api_key: str | None = None

  jwt_secret_key: str = "change-this-in-production"
  jwt_algorithm: str = "HS256"
  access_token_expire_minutes: int = 60

  model_config = SettingsConfigDict(
    env_file=[
      Path(__file__).resolve().parents[1] / "api" / ".env",
      Path(__file__).resolve().parents[2] / ".env",
      Path(__file__).resolve().parents[3] / ".env",
    ],
    extra="ignore",
  )

  @model_validator(mode="after")
  def check_production_defaults(self):
      if self.app_env == "production":
          if self.jwt_secret_key == "change-this-in-production":
              raise ValueError("Insecure JWT secret 'change-this-in-production' is forbidden in production.")
          if self.app_debug:
              raise ValueError("Debug mode must be disabled in production.")
          if self.cors_allowed_origins == "http://localhost:5173" or "*" in self.cors_allowed_origins:
              pass # Just a warning or strict check, but document says don't deploy with allow_origins=["*"]
      return self

settings = Settings()