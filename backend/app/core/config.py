from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Localhost for local dev
    database_url: str = "postgresql://app:app@localhost:5432/praijing"

    class Config:
        env_file = ".env"


settings = Settings()
