from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    environment: str = "dev"

    class Config:
        env_file = ".env"      # local dev only
        env_file_encoding = "utf-8"

settings = Settings()
